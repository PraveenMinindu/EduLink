// =============================================================
// EduLink Admin — API Service
// All HTTP calls to FastAPI backend
// =============================================================

import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/university.dart';
import '../models/degree_program.dart';
import '../models/admin_user.dart';
import 'auth_service.dart';

class ApiService {

  // Fix 1: void Function() avoids importing Flutter UI types (VoidCallback is Flutter)
  // Fix 2: _sessionExpiredOnce prevents duplicate callback invocations
  static void Function()? onSessionExpired;
  static bool _sessionExpiredOnce = false;

  static void _fireSessionExpired() {
    if (_sessionExpiredOnce) return;
    _sessionExpiredOnce = true;
    onSessionExpired?.call();
  }

  // Call this on successful login to reset the guard for the new session
  static void resetSessionGuard() => _sessionExpiredOnce = false;

  // ── Shared headers ────────────────────────────────────────
  static Future<Map<String, String>> _headers() async {
    String? token;
    try {
      token = await AuthService.getToken();
    } catch (_) {
      _fireSessionExpired();
      throw Exception('Session expired. Please sign in again.');
    }
    return {
      'Content-Type':  'application/json',
      'Authorization': 'Bearer ${token ?? ""}',
    };
  }

  static Map<String, dynamic> _decode(http.Response res) {
    if (res.statusCode == 401 || res.statusCode == 403) {
      _fireSessionExpired();
      throw Exception('Session expired. Please sign in again.');
    }
    if (res.statusCode >= 400) {
      final body = jsonDecode(res.body);
      throw Exception(body['detail'] ?? 'Request failed (${res.statusCode})');
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }

  // ══════════════════════════════════════════════════════════
  // ADMIN PROFILE
  // ══════════════════════════════════════════════════════════

  static Future<AdminUser> updateProfile({required String name}) async {
    final res = await http.patch(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.me}'),
      headers: await _headers(),
      body:    jsonEncode({'name': name}),
    ).timeout(ApiConfig.defaultTimeout);
    return AdminUser.fromJson(_decode(res));
  }

  // ══════════════════════════════════════════════════════════
  // DASHBOARD
  // ══════════════════════════════════════════════════════════

  static Future<Map<String, dynamic>> getStats() async {
    final res = await http.get(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.stats}'),
      headers: await _headers(),
    ).timeout(ApiConfig.defaultTimeout);
    return _decode(res)['data'] as Map<String, dynamic>;
  }

  // ══════════════════════════════════════════════════════════
  // UNIVERSITIES
  // ══════════════════════════════════════════════════════════

  static Future<List<University>> getUniversities({
    String? status,
    String? search,
  }) async {
    final params = <String, String>{};
    if (status != null && status.isNotEmpty) params['status'] = status;
    if (search != null && search.isNotEmpty) params['search'] = search;

    final uri = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.universities}')
        .replace(queryParameters: params.isEmpty ? null : params);

    final res = await http.get(
      uri,
      headers: await _headers(),
    ).timeout(ApiConfig.defaultTimeout);

    final body = _decode(res);
    final list  = body['data'] as List<dynamic>;
    return list.map((j) => University.fromJson(j as Map<String, dynamic>)).toList();
  }

  static Future<University> getUniversity(String id) async {
    final res = await http.get(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.universities}/$id'),
      headers: await _headers(),
    ).timeout(ApiConfig.defaultTimeout);
    return University.fromJson(_decode(res)['data'] as Map<String, dynamic>);
  }

  static Future<University> createUniversity(Map<String, dynamic> data) async {
    final res = await http.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.universities}'),
      headers: await _headers(),
      body:    jsonEncode(data),
    ).timeout(ApiConfig.defaultTimeout);
    return University.fromJson(_decode(res)['data'] as Map<String, dynamic>);
  }

  static Future<University> updateUniversity(
    String id,
    Map<String, dynamic> data,
  ) async {
    final res = await http.patch(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.universities}/$id'),
      headers: await _headers(),
      body:    jsonEncode(data),
    ).timeout(ApiConfig.defaultTimeout);
    return University.fromJson(_decode(res)['data'] as Map<String, dynamic>);
  }

  static Future<void> deleteUniversity(String id) async {
    final res = await http.delete(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.universities}/$id'),
      headers: await _headers(),
    ).timeout(ApiConfig.defaultTimeout);
    _decode(res);
  }

  // ══════════════════════════════════════════════════════════
  // DEGREE PROGRAMS
  // ══════════════════════════════════════════════════════════

  static Future<List<DegreeProgram>> getPrograms({
    String? universityId,
    String? status,
    String? search,
  }) async {
    final params = <String, String>{};
    if (universityId != null && universityId.isNotEmpty)
      params['universityId'] = universityId;
    if (status != null && status.isNotEmpty) params['status'] = status;
    if (search != null && search.isNotEmpty)  params['search'] = search;

    final uri = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.programs}')
        .replace(queryParameters: params.isEmpty ? null : params);

    final res = await http.get(
      uri,
      headers: await _headers(),
    ).timeout(ApiConfig.defaultTimeout);

    final body = _decode(res);
    final list  = body['data'] as List<dynamic>;
    return list
        .map((j) => DegreeProgram.fromJson(j as Map<String, dynamic>))
        .toList();
  }

  static Future<DegreeProgram> getProgram(String id) async {
    final res = await http.get(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.programs}/$id'),
      headers: await _headers(),
    ).timeout(ApiConfig.defaultTimeout);
    return DegreeProgram.fromJson(
        _decode(res)['data'] as Map<String, dynamic>);
  }

  static Future<DegreeProgram> createProgram(Map<String, dynamic> data) async {
    final res = await http.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.programs}'),
      headers: await _headers(),
      body:    jsonEncode(data),
    ).timeout(ApiConfig.defaultTimeout);
    return DegreeProgram.fromJson(
        _decode(res)['data'] as Map<String, dynamic>);
  }

  static Future<DegreeProgram> updateProgram(
    String id,
    Map<String, dynamic> data,
  ) async {
    final res = await http.patch(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.programs}/$id'),
      headers: await _headers(),
      body:    jsonEncode(data),
    ).timeout(ApiConfig.defaultTimeout);
    return DegreeProgram.fromJson(
        _decode(res)['data'] as Map<String, dynamic>);
  }

  /// Soft delete — sets status=Inactive on the backend
  static Future<void> deactivateProgram(String id) async {
    final res = await http.delete(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.programs}/$id'),
      headers: await _headers(),
    ).timeout(ApiConfig.defaultTimeout);
    _decode(res);
  }
}
