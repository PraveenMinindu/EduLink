import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../services/auth_service.dart';
import 'mcq_screen.dart';
import 'login_screen.dart';
import 'report/report_screen.dart';

class DashboardScreen extends StatefulWidget {
  final String studentId;
  const DashboardScreen({super.key, required this.studentId});
  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List<Map<String, dynamic>> _assessments = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    setState(() => _loading = true);
    final history =
        await AuthService.getAssessmentHistory(widget.studentId);
    if (mounted) {
      setState(() {
        _assessments = history;
        _loading = false;
      });
    }
  }

  Future<void> _startNewAssessment() async {
    final assessmentId =
        AuthService.generateAssessmentId(widget.studentId);
    if (mounted) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => MCQScreen(
            studentId:    widget.studentId,
            assessmentId: assessmentId,
          ),
        ),
      );
    }
  }

  Future<void> _signOut() async {
    await AuthService.signOut();
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Column(
        children: [
          // ── Header ──────────────────────────────────────
          Container(
            color: AppColors.navy,
            padding: const EdgeInsets.fromLTRB(22, 54, 22, 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      "EduLink",
                      style: GoogleFonts.playfairDisplay(
                        fontSize: 26,
                        color: Colors.white,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    IconButton(
                      onPressed: _signOut,
                      icon: const Icon(Icons.logout,
                          color: Colors.white54, size: 20),
                      tooltip: "Sign out",
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  "Your Career Assessments",
                  style: TextStyle(
                    fontSize: 13,
                    color: Colors.white.withOpacity(0.6),
                  ),
                ),
              ],
            ),
          ),

          // ── Body ─────────────────────────────────────────
          Expanded(
            child: _loading
                ? const Center(
                    child: CircularProgressIndicator(
                        color: AppColors.navy))
                : RefreshIndicator(
                    onRefresh: _loadHistory,
                    child: ListView(
                      padding: const EdgeInsets.all(16),
                      children: [

                        // Start new assessment button
                        GestureDetector(
                          onTap: _startNewAssessment,
                          child: Container(
                            width: double.infinity,
                            padding: const EdgeInsets.all(18),
                            decoration: BoxDecoration(
                              color: AppColors.navy,
                              borderRadius: BorderRadius.circular(16),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.add_circle_outline,
                                    color: Colors.white, size: 24),
                                const SizedBox(width: 14),
                                Column(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      "Start New Assessment",
                                      style:
                                          GoogleFonts.playfairDisplay(
                                        fontSize: 16,
                                        color: Colors.white,
                                        fontWeight: FontWeight.w600,
                                      ),
                                    ),
                                    Text(
                                      "Get a fresh career recommendation",
                                      style: TextStyle(
                                        fontSize: 12,
                                        color: Colors.white
                                            .withOpacity(0.65),
                                      ),
                                    ),
                                  ],
                                ),
                                const Spacer(),
                                const Icon(Icons.arrow_forward_ios,
                                    color: Colors.white54, size: 16),
                              ],
                            ),
                          ),
                        ),

                        const SizedBox(height: 20),

                        // Assessment history
                        if (_assessments.isEmpty)
                          Center(
                            child: Padding(
                              padding: const EdgeInsets.all(40),
                              child: Text(
                                "No assessments yet.\nStart your first one above.",
                                textAlign: TextAlign.center,
                                style: const TextStyle(
                                  color: AppColors.text3,
                                  fontSize: 14,
                                  height: 1.6,
                                ),
                              ),
                            ),
                          )
                        else ...[
                          Text(
                            "PREVIOUS ASSESSMENTS",
                            style: const TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w700,
                              color: AppColors.text3,
                              letterSpacing: 0.5,
                            ),
                          ),
                          const SizedBox(height: 10),
                          ..._assessments
                              .asMap()
                              .entries
                              .map((entry) {
                            final i = entry.key;
                            final a = entry.value;
                            final isLatest = i == 0;
                            return _assessmentCard(a, isLatest);
                          }),
                        ],
                      ],
                    ),
                  ),
          ),
        ],
      ),
    );
  }

  Widget _assessmentCard(
      Map<String, dynamic> assessment, bool isLatest) {
    final role         = assessment['role'] ?? 'Unknown Role';
    final score        = (assessment['score'] ?? 0.0).toDouble();
    final confidence   = assessment['confidence'] ?? 'Medium';
    final date         = assessment['date'] ?? '';
    final assessmentId = assessment['assessment_id'] ?? '';
    final cluster =
        (assessment['cluster'] ?? '').toString().replaceAll('_', ' ');

    Color confidenceColor;
    if (confidence == 'High')
      confidenceColor = AppColors.mint;
    else if (confidence == 'Medium')
      confidenceColor = AppColors.gold;
    else
      confidenceColor = AppColors.rose;

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isLatest ? AppColors.navy : AppColors.border,
          width: isLatest ? 1.5 : 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              if (isLatest)
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: AppColors.navy,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: const Text(
                    "LATEST",
                    style: TextStyle(
                      fontSize: 9,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                      letterSpacing: 0.5,
                    ),
                  ),
                ),
              if (isLatest) const SizedBox(width: 8),
              Text(
                date,
                style: const TextStyle(
                  fontSize: 11,
                  color: AppColors.text3,
                ),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(
                    horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: confidenceColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  confidence,
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w700,
                    color: confidenceColor,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Text(
            role,
            style: GoogleFonts.playfairDisplay(
              fontSize: 18,
              color: AppColors.navy,
              fontWeight: FontWeight.w700,
            ),
          ),
          Text(
            cluster,
            style: const TextStyle(
              fontSize: 12,
              color: AppColors.text3,
            ),
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Text(
                "Score: ${score.toStringAsFixed(1)}/100",
                style: const TextStyle(
                  fontSize: 12,
                  color: AppColors.text2,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const Spacer(),
              if (assessmentId.isNotEmpty)
                GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            ReportScreen(studentId: assessmentId),
                      ),
                    );
                  },
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 14, vertical: 8),
                    decoration: BoxDecoration(
                      color: AppColors.navy,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Text(
                      "View Report",
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ],
      ),
    );
  }
}
