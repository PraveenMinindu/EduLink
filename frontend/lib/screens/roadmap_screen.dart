import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/app_colors.dart';
import '../../models/career_report_model.dart';

// =============================================================
// Career Roadmap Screen — Removed
//
// Predicting a student's future career path is outside the
// scope of EduLink. Career directions change over time based
// on personal growth, industry shifts, and life decisions
// that cannot be predicted from a single psychometric
// assessment.
//
// This screen now shows the student's current psychological
// strengths derived from their assessment results, along with
// a recommendation to seek professional career counselling
// for long-term career planning.
// =============================================================

class RoadmapScreen extends StatelessWidget {
  final CareerReport report;
  const RoadmapScreen({super.key, required this.report});

  @override
  Widget build(BuildContext context) {
    final role = report.finalRole;
    final cluster = report.top1Cluster.replaceAll('_', ' ');

    // Build strength list from real writing and MCQ scores
    final strengths = <String>[];
    if (report.writingAnalytical >= 60) strengths.add("Analytical thinking");
    if (report.writingClarity >= 60) strengths.add("Clear communication");
    if (report.writingConfidence >= 60) strengths.add("Confidence");
    if (report.writingCreativity >= 60) strengths.add("Creative thinking");
    if (report.writingStructure >= 60) strengths.add("Structured reasoning");
    if (strengths.isEmpty) strengths.add("Technical aptitude");

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        backgroundColor: AppColors.navy,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          "Your Strengths",
          style: GoogleFonts.playfairDisplay(
            color: Colors.white,
            fontSize: 18,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Recommended role card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.navy,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Recommended Career",
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.7),
                      fontSize: 12,
                      letterSpacing: 0.5,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    role,
                    style: GoogleFonts.playfairDisplay(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    cluster,
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.6),
                      fontSize: 13,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Strengths section
            Text(
              "Your Identified Strengths",
              style: GoogleFonts.playfairDisplay(
                fontSize: 17,
                fontWeight: FontWeight.w700,
                color: AppColors.text1,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              "Based on your psychometric assessment and writing analysis.",
              style: TextStyle(fontSize: 12, color: AppColors.text3),
            ),
            const SizedBox(height: 14),

            ...strengths.map(
              (s) => Container(
                margin: const EdgeInsets.only(bottom: 10),
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 14,
                ),
                decoration: BoxDecoration(
                  color: AppColors.card,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.border),
                ),
                child: Row(
                  children: [
                    const Icon(
                      Icons.check_circle_outline,
                      color: Color(0xFF4CAF50),
                      size: 20,
                    ),
                    const SizedBox(width: 12),
                    Text(
                      s,
                      style: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: AppColors.text1,
                      ),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Advisory note
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: AppColors.card,
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: AppColors.border),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(
                        Icons.info_outline,
                        color: AppColors.blue,
                        size: 20,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        "About Career Planning",
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: AppColors.text1,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    "EduLink provides career guidance based on your current psychometric profile and market data. Career paths evolve over time as you develop new skills and interests.",
                    style: TextStyle(
                      fontSize: 13,
                      color: AppColors.text2,
                      height: 1.5,
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    "For long-term career planning, we recommend speaking with a professional career counsellor or your institution's career guidance service.",
                    style: TextStyle(
                      fontSize: 13,
                      color: AppColors.text2,
                      height: 1.5,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}
