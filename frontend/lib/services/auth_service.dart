import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class AuthService {
  static final FirebaseAuth _auth = FirebaseAuth.instance;
  static final FirebaseFirestore _db = FirebaseFirestore.instance;

  // ── Existing methods — unchanged ──────────────────────────

  static User? get currentUser => _auth.currentUser;

  static Future<UserCredential?> signIn(
      String email, String password) async {
    return await _auth.signInWithEmailAndPassword(
        email: email, password: password);
  }

  static Future<UserCredential?> register(
      String email, String password) async {
    return await _auth.createUserWithEmailAndPassword(
        email: email, password: password);
  }

  static Future<void> signOut() async => await _auth.signOut();

  static Stream<User?> get authStateChanges => _auth.authStateChanges();

  // ── New v2 methods ────────────────────────────────────────

  /// Save Firebase UID → studentId mapping after registration.
  static Future<void> saveUserMapping(
      String studentId, String name) async {
    final uid = _auth.currentUser?.uid;
    if (uid == null) return;
    await _db.collection('user_mappings').doc(uid).set({
      'student_id': studentId,
      'name': name,
      'created_at': DateTime.now().toIso8601String(),
    });
  }

  /// Get studentId from Firebase UID after login.
  /// Returns null if no mapping found.
  static Future<String?> getStudentId() async {
    final uid = _auth.currentUser?.uid;
    if (uid == null) return null;
    final doc = await _db.collection('user_mappings').doc(uid).get();
    if (doc.exists) {
      return doc.data()?['student_id'] as String?;
    }
    return null;
  }

  /// Check if student has any assessment history.
  static Future<bool> hasAssessmentHistory(String studentId) async {
    final doc = await _db
        .collection('assessment_history')
        .doc(studentId)
        .get();
    if (!doc.exists) return false;
    final assessments = doc.data()?['assessments'] as List?;
    return assessments != null && assessments.isNotEmpty;
  }

  /// Get all assessments for a student, newest first.
  static Future<List<Map<String, dynamic>>> getAssessmentHistory(
      String studentId) async {
    final doc = await _db
        .collection('assessment_history')
        .doc(studentId)
        .get();
    if (!doc.exists) return [];
    final raw = doc.data()?['assessments'] as List? ?? [];
    final list = raw.map((e) => Map<String, dynamic>.from(e)).toList();
    list.sort((a, b) =>
        (b['date'] ?? '').compareTo(a['date'] ?? ''));
    return list;
  }

  /// Generate a unique assessmentId from studentId + timestamp.
  static String generateAssessmentId(String studentId) {
    final now = DateTime.now();
    final ts =
        '${now.year}${now.month.toString().padLeft(2, '0')}${now.day.toString().padLeft(2, '0')}'
        '_${now.hour.toString().padLeft(2, '0')}${now.minute.toString().padLeft(2, '0')}${now.second.toString().padLeft(2, '0')}';
    return '${studentId}_$ts';
  }
}
