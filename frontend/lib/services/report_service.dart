import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/career_report_model.dart';

class ReportService {
  static final FirebaseFirestore _db = FirebaseFirestore.instance;

  // Listen to report status in real time
  static Stream<DocumentSnapshot> statusStream(String studentId) {
    return _db.collection('report_status').doc(studentId).snapshots();
  }

  // Get career report from Firestore
  static Future<CareerReport?> getReport(String studentId) async {
    final doc = await _db.collection('career_reports').doc(studentId).get();
    if (!doc.exists) return null;
    return CareerReport.fromJson(doc.data()!);
  }
}
