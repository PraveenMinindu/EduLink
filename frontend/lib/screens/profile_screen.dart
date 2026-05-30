import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/app_colors.dart';
import '../../models/career_report_model.dart';
import '../../services/auth_service.dart';
import 'login_screen.dart';
import 'mcq_screen.dart';
import 'writing_tips_screen.dart';
import 'report/education_screen.dart';

class ProfileScreen extends StatelessWidget {
  final String studentId;
  final CareerReport report;

  const ProfileScreen({
    super.key,
    required this.studentId,
    required this.report,
  });

  // Get initials from name
  String _initials(String name) {
    final parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return "${parts[0][0]}${parts[1][0]}".toUpperCase();
    }
    if (name.length >= 2) return name.substring(0, 2).toUpperCase();
    return name.toUpperCase();
  }

  @override
  Widget build(BuildContext context) {
    final displayName = report.studentName.isNotEmpty
        ? report.studentName
        : studentId;

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Column(
        children: [
          // Profile hero
          Container(
            color: AppColors.navy,
            padding: const EdgeInsets.fromLTRB(22, 54, 22, 28),
            width: double.infinity,
            child: Column(
              children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: GestureDetector(
                    onTap: () => Navigator.pop(context),
                    child: Row(
                      children: [
                        const Icon(
                          Icons.arrow_back_ios,
                          color: Colors.white54,
                          size: 16,
                        ),
                        const Text(
                          "Report",
                          style: TextStyle(color: Colors.white54, fontSize: 13),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // Avatar with initials from real name
                Container(
                  width: 72,
                  height: 72,
                  decoration: const BoxDecoration(
                    color: AppColors.blue,
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: Text(
                      _initials(displayName),
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.w700,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 12),

                // Show real student name
                Text(
                  displayName,
                  style: GoogleFonts.playfairDisplay(
                    fontSize: 20,
                    color: Colors.white,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  report.finalRole,
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.white.withOpacity(0.5),
                  ),
                ),
                const SizedBox(height: 18),

                // Stats row
                Container(
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.07),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Row(
                    children: [
                      _stat(report.finalScore.toStringAsFixed(1), "AI Score"),
                      _vDivider(),
                      _stat(report.confidenceLabel, "Confidence"),
                      _vDivider(),
                      _stat("1", "Assessments"),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Body
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  // Retake card
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [Color(0xFFEFF6FF), Color(0xFFF5F3FF)],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.blueMid),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          "Retake assessment",
                          style: TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.w700,
                            color: AppColors.navy,
                          ),
                        ),
                        const SizedBox(height: 5),
                        const Text(
                          "Your interests and skills may have changed. A fresh assessment gives you updated career guidance.",
                          style: TextStyle(
                            fontSize: 12,
                            color: AppColors.text2,
                            height: 1.5,
                          ),
                        ),
                        const SizedBox(height: 12),
                        ...[
                          "You have learned new skills or taken new courses",
                          "Your career interests have changed",
                          "It has been more than 6 months since your last assessment",
                        ].map(
                          (reason) => Padding(
                            padding: const EdgeInsets.only(bottom: 6),
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Container(
                                  width: 6,
                                  height: 6,
                                  margin: const EdgeInsets.only(
                                    top: 5,
                                    right: 8,
                                  ),
                                  decoration: const BoxDecoration(
                                    color: AppColors.blue,
                                    shape: BoxShape.circle,
                                  ),
                                ),
                                Expanded(
                                  child: Text(
                                    reason,
                                    style: const TextStyle(
                                      fontSize: 12,
                                      color: AppColors.text2,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 14),
                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton(
                            onPressed: () => Navigator.pushAndRemoveUntil(
                              context,
                              MaterialPageRoute(
                                builder: (_) => MCQScreen(studentId: studentId),
                              ),
                              (route) => false,
                            ),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: AppColors.blue,
                              padding: const EdgeInsets.symmetric(vertical: 14),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                            child: Text(
                              "Start new assessment →",
                              style: GoogleFonts.plusJakartaSans(
                                fontSize: 14,
                                fontWeight: FontWeight.w600,
                                color: Colors.white,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Assessment history
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.card,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          "ASSESSMENT HISTORY",
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w700,
                            color: AppColors.text3,
                            letterSpacing: 0.5,
                          ),
                        ),
                        const SizedBox(height: 12),
                        _historyItem(
                          color: AppColors.mint,
                          date: "Today",
                          role: report.finalRole,
                          conf: report.confidenceLabel,
                          score: report.finalScore,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Menu
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.card,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      children: [
                        _menuItem(
                          context,
                          Icons.bar_chart_rounded,
                          AppColors.bluePale,
                          "View my report",
                          () => Navigator.pop(context),
                        ),
                        _menuItem(
                          context,
                          Icons.school_outlined,
                          AppColors.mintPale,
                          "Education paths",
                          () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => EducationScreen(report: report),
                            ),
                          ),
                        ),
                        _menuItem(
                          context,
                          Icons.edit_note,
                          AppColors.violetPale,
                          "Writing tips",
                          () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => WritingTipsScreen(report: report),
                            ),
                          ),
                        ),
                        _menuItem(
                          context,
                          Icons.logout,
                          AppColors.rosePale,
                          "Sign out",
                          () async {
                            await AuthService.signOut();
                            if (context.mounted) {
                              Navigator.pushAndRemoveUntil(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => const LoginScreen(),
                                ),
                                (route) => false,
                              );
                            }
                          },
                          textColor: AppColors.rose,
                          showDivider: false,
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _stat(String value, String label) => Expanded(
    child: Padding(
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Column(
        children: [
          Text(
            value,
            style: GoogleFonts.playfairDisplay(
              fontSize: 18,
              color: Colors.white,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 3),
          Text(
            label,
            style: TextStyle(
              fontSize: 9,
              color: Colors.white.withOpacity(0.5),
              letterSpacing: 0.3,
            ),
          ),
        ],
      ),
    ),
  );

  Widget _vDivider() =>
      Container(width: 1, height: 36, color: Colors.white.withOpacity(0.1));

  Widget _historyItem({
    required Color color,
    required String date,
    required String role,
    required String conf,
    required double score,
  }) => Row(
    children: [
      Container(
        width: 10,
        height: 10,
        decoration: BoxDecoration(color: color, shape: BoxShape.circle),
      ),
      const SizedBox(width: 10),
      Expanded(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              date,
              style: const TextStyle(fontSize: 11, color: AppColors.text3),
            ),
            Text(
              role,
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: AppColors.text1,
              ),
            ),
          ],
        ),
      ),
      Container(
        padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 3),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          "$conf · ${score.toStringAsFixed(1)}",
          style: TextStyle(
            fontSize: 10,
            fontWeight: FontWeight.w700,
            color: color,
          ),
        ),
      ),
    ],
  );

  Widget _menuItem(
    BuildContext context,
    IconData icon,
    Color iconBg,
    String label,
    VoidCallback onTap, {
    Color? textColor,
    bool showDivider = true,
  }) => Column(
    children: [
      GestureDetector(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 10),
          child: Row(
            children: [
              Container(
                width: 36,
                height: 36,
                decoration: BoxDecoration(
                  color: iconBg,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Icon(icon, size: 18, color: textColor ?? AppColors.navy),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  label,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: textColor ?? AppColors.text1,
                  ),
                ),
              ),
              const Icon(Icons.chevron_right, color: AppColors.border),
            ],
          ),
        ),
      ),
      if (showDivider) Divider(height: 1, color: AppColors.surface),
    ],
  );
}
