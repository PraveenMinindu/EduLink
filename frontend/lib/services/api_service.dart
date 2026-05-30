import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config/app_constants.dart';
import 'dart:async';

class ApiService {
  static const String _base = AppConstants.baseUrl;

  // ── Timeouts ──────────────────────────────────────────────
  // MCQ/Writing: 120s — SentenceTransformer loads on first call
  // Report:      180s — full 7-model pipeline takes 60-90s
  // General GET:  60s — status polling and report retrieval
  static const _shortTimeout = Duration(seconds: 60);
  static const _mcqTimeout = Duration(seconds: 120);
  static const _reportTimeout = Duration(seconds: 180);

  static Future<Map<String, dynamic>> _post(
    String path,
    Map<String, dynamic> body, {
    Duration? timeout,
  }) async {
    try {
      final res = await http
          .post(
            Uri.parse('$_base$path'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(body),
          )
          .timeout(timeout ?? _shortTimeout);
      return jsonDecode(res.body);
    } catch (e) {
      print('API Error on $path: $e');
      return {'status': 'error', 'message': e.toString()};
    }
  }

  static Future<Map<String, dynamic>> _get(
    String path, {
    Duration? timeout,
  }) async {
    try {
      final res = await http
          .get(Uri.parse('$_base$path'))
          .timeout(timeout ?? _shortTimeout);
      return jsonDecode(res.body);
    } catch (e) {
      print('API Error on $path: $e');
      return {'status': 'error', 'message': e.toString()};
    }
  }

  // ── Endpoints ─────────────────────────────────────────────

  static Future<Map<String, dynamic>> registerStudent(
    Map<String, dynamic> data,
  ) => _post('/student/register', data);

  // MCQ uses 120s timeout — model may load on first call
  static Future<Map<String, dynamic>> submitMCQ(Map<String, dynamic> data) =>
      _post('/student/submit-mcq', data, timeout: _mcqTimeout);

  // Writing uses 120s timeout — same reason
  static Future<Map<String, dynamic>> submitWriting(
    String studentId,
    String text,
  ) => _post('/student/submit-writing', {
    'student_id': studentId,
    'text': text,
  }, timeout: _mcqTimeout);

  // Generate report uses 180s — full 7-model pipeline
  static Future<Map<String, dynamic>> generateReport(String studentId) async {
    try {
      final res = await http
          .post(Uri.parse('$_base/student/generate-report/$studentId'))
          .timeout(_reportTimeout);
      return jsonDecode(res.body);
    } catch (e) {
      print('API Error on generate-report: $e');
      return {'status': 'error', 'message': e.toString()};
    }
  }

  static Future<Map<String, dynamic>> getReport(String studentId) =>
      _get('/student/report/$studentId');

  static Future<Map<String, dynamic>> getStatus(String studentId) =>
      _get('/student/report-status/$studentId');

  static Future<Map<String, dynamic>> getProfile(String studentId) =>
      _get('/student/profile/$studentId');

  static Future<Map<String, dynamic>> getSkills(String studentId) =>
      _get('/student/skills/$studentId', timeout: _mcqTimeout);
}
