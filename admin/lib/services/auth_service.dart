// =============================================================
// EduLink Admin — Auth Service
// Fix: removed SharedPreferences (unused), simplified signOut
// Firebase token is always fetched fresh via getIdToken()
// =============================================================

import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import 'api_service.dart';
import '../models/admin_user.dart';

class AuthService {

  // ── Sign in ──────────────────────────────────────────────
  static Future<AdminUser> signIn(String email, String password) async {
    // Step 1: Firebase Auth client-side
    final cred = await FirebaseAuth.instance.signInWithEmailAndPassword(
      email:    email,
      password: password,
    );

    // Step 2: Get fresh ID token
    final idToken = await cred.user!.getIdToken();
    if (idToken == null) throw Exception('Could not get ID token.');

    // Step 3: Verify admin role with backend
    final res = await http
        .post(
          Uri.parse('${ApiConfig.baseUrl}${ApiConfig.login}'),
          headers: {'Content-Type': 'application/json'},
          body:    jsonEncode({'idToken': idToken}),
        )
        .timeout(ApiConfig.defaultTimeout);

    if (res.statusCode == 403) {
      await FirebaseAuth.instance.signOut();
      throw Exception(
          'Access denied. This account is not an administrator.');
    }

    if (res.statusCode != 200) {
      await FirebaseAuth.instance.signOut();
      final body = jsonDecode(res.body);
      throw Exception(body['detail'] ?? 'Authentication failed.');
    }

    final data = jsonDecode(res.body);
    // Reset session expiry guard so a fresh session works cleanly
    ApiService.resetSessionGuard();
    return AdminUser.fromJson(data);
  }

  // ── Sign out ─────────────────────────────────────────────
  static Future<void> signOut() async {
    await FirebaseAuth.instance.signOut();
  }

  // ── Get current Firebase ID token (auto-refreshed) ──────
  static Future<String?> getToken() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return null;
    return await user.getIdToken();
  }

  // ── Get current admin profile from backend ───────────────
  static Future<AdminUser?> getMe() async {
    final token = await getToken();
    if (token == null) return null;

    try {
      final res = await http
          .get(
            Uri.parse('${ApiConfig.baseUrl}${ApiConfig.me}'),
            headers: {
              'Authorization': 'Bearer $token',
              'Content-Type':  'application/json',
            },
          )
          .timeout(ApiConfig.defaultTimeout);

      if (res.statusCode != 200) return null;
      final data = jsonDecode(res.body);
      return AdminUser.fromJson(data);
    } catch (_) {
      return null;
    }
  }

  // ── Check if signed in ───────────────────────────────────
  static bool get isSignedIn =>
      FirebaseAuth.instance.currentUser != null;

  // ── Change password ──────────────────────────────────────
  // Re-authenticates with the current password before changing it —
  // Firebase requires a recent sign-in for sensitive account changes,
  // and this also acts as the "confirm current password" check.
  static Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null || user.email == null) {
      throw Exception('Not signed in.');
    }

    try {
      final cred = EmailAuthProvider.credential(
        email:    user.email!,
        password: currentPassword,
      );
      await user.reauthenticateWithCredential(cred);
      await user.updatePassword(newPassword);
    } on FirebaseAuthException catch (e) {
      throw Exception(_authErrorMessage(e));
    }
  }

  static String _authErrorMessage(FirebaseAuthException e) {
    switch (e.code) {
      case 'wrong-password':
      case 'invalid-credential':
        return 'Current password is incorrect.';
      case 'weak-password':
        return 'New password is too weak. Use at least 6 characters.';
      case 'requires-recent-login':
        return 'Please sign out and sign in again, then retry.';
      case 'too-many-requests':
        return 'Too many attempts. Please try again later.';
      default:
        return e.message ?? 'Could not update password.';
    }
  }
}
