import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config/app_constants.dart';
import 'dart:async';

class ApiService {
  static const String _base = AppConstants.baseUrl;

  static const _shortTimeout  = Duration(seconds: 60);
  static const _mcqTimeout    = Duration(seconds: 120);
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

  // ── Existing endpoints — unchanged ────────────────────────

  static Future<Map<String, dynamic>> registerStudent(
    Map<String, dynamic> data,
  ) => _post('/student/register', data);

  static Future<Map<String, dynamic>> submitMCQ(
          Map<String, dynamic> data) =>
      _post('/student/submit-mcq', data, timeout: _mcqTimeout);

  static Future<Map<String, dynamic>> submitWriting(
    String studentId,
    String text,
  ) =>
      _post('/student/submit-writing', {
        'student_id': studentId,
        'text': text,
      }, timeout: _mcqTimeout);

  static Future<Map<String, dynamic>> generateReport(
      String studentId) async {
    try {
      final res = await http
          .post(Uri.parse(
              '$_base/student/generate-report/$studentId'))
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

  // ── V2 endpoints — assessment-based ─────────────────────

  static Future<Map<String, dynamic>> submitMCQv2(
    String assessmentId,
    Map<String, dynamic> answers,
  ) =>
      _post('/student/submit-mcq-v2', {
        'assessment_id': assessmentId,
        ...answers,
      }, timeout: _mcqTimeout);

  static Future<Map<String, dynamic>> submitWritingV2(
    String assessmentId,
    String text,
  ) =>
      _post('/student/submit-writing-v2', {
        'assessment_id': assessmentId,
        'text': text,
      }, timeout: _mcqTimeout);

  static Future<Map<String, dynamic>> generateReportV2(
      String assessmentId) async {
    try {
      final res = await http
          .post(Uri.parse(
              '$_base/student/generate-report-v2/$assessmentId'))
          .timeout(_reportTimeout);
      return jsonDecode(res.body);
    } catch (e) {
      print('API Error on generate-report-v2: $e');
      return {'status': 'error', 'message': e.toString()};
    }
  }

  static Future<Map<String, dynamic>> getReportV2(
          String assessmentId) =>
      _get('/student/report-v2/$assessmentId');

  static Future<Map<String, dynamic>> getStatusV2(
          String assessmentId) =>
      _get('/student/report-status-v2/$assessmentId');

  static Future<Map<String, dynamic>> getAssessmentHistory(
          String studentId) =>
      _get('/student/history/$studentId');
}
