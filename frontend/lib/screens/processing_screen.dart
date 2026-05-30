import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../config/app_colors.dart';
import 'report/report_screen.dart';

class ProcessingScreen extends StatelessWidget {
  final String studentId;
  const ProcessingScreen({super.key, required this.studentId});

  static const _steps = [
    "Career fit prediction",
    "Writing analysis",
    "Salary prediction",
    "Job demand forecasting",
    "Education path recommendation",
    "Vacancy matching",
    "AI reasoning layer",
  ];

  // Map backend status message to step index
  int _activeStep(String message) {
    final m = message.toLowerCase();
    if (m.contains('career') || m.contains('fit'))      return 0;
    if (m.contains('writing'))                          return 1;
    if (m.contains('salary'))                          return 2;
    if (m.contains('demand') || m.contains('job demand'))return 3;
    if (m.contains('education'))                       return 4;
    if (m.contains('vacancy') || m.contains('jobs'))   return 5;
    if (m.contains('reasoning') || m.contains('ai'))   return 6;
    return 3; // default middle
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.navy,
      body: StreamBuilder<DocumentSnapshot>(
        stream: FirebaseFirestore.instance
            .collection('report_status')
            .doc(studentId)
            .snapshots(),
        builder: (context, snapshot) {
          final data    = snapshot.data?.data() as Map<String, dynamic>?;
          final status  = data?['status']  ?? 'pending';
          final message = data?['message'] ?? 'Analysing your profile...';

          // Navigate to report when done
          if (status == 'done') {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (_) => ReportScreen(studentId: studentId),
                ),
              );
            });
          }

          // Show error if failed
          if (status == 'error') {
            return Padding(
              padding: const EdgeInsets.all(28),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline,
                      color: AppColors.rose, size: 52),
                  const SizedBox(height: 20),
                  Text(
                    "Something went wrong",
                    style: GoogleFonts.playfairDisplay(
                      fontSize: 24,
                      color: Colors.white,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    message,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 13,
                      color: Colors.white.withOpacity(0.6),
                    ),
                  ),
                  const SizedBox(height: 28),
                  ElevatedButton(
                    onPressed: () => Navigator.pop(context),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.blue,
                      padding: const EdgeInsets.symmetric(
                          horizontal: 32, vertical: 14),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12)),
                    ),
                    child: const Text("Go back",
                        style: TextStyle(color: Colors.white)),
                  ),
                ],
              ),
            );
          }

          final activeIdx = status == 'done'
              ? _steps.length
              : _activeStep(message);

          return Padding(
            padding: const EdgeInsets.all(28),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Spinner
                const SizedBox(
                  width: 52,
                  height: 52,
                  child: CircularProgressIndicator(
                    color: Color(0xFF60A5FA),
                    strokeWidth: 2.5,
                  ),
                ),
                const SizedBox(height: 24),

                // Title
                Text(
                  "Analysing your profile",
                  style: GoogleFonts.playfairDisplay(
                    fontSize: 26,
                    color: Colors.white,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 8),

                // Real status message from Backend
                Text(
                  message,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 13,
                    color: Colors.white.withOpacity(0.5),
                    height: 1.6,
                  ),
                ),
                const SizedBox(height: 28),

                // Steps list
                Container(
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.05),
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(
                        color: Colors.white.withOpacity(0.09)),
                  ),
                  child: Column(
                    children: _steps.asMap().entries.map((e) {
                      final idx  = e.key;
                      final step = e.value;
                      final isDone   = status == 'done' || idx < activeIdx;
                      final isActive = status == 'processing' &&
                                       idx == activeIdx;

                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 7),
                        child: Row(children: [
                          // Icon circle
                          Container(
                            width: 26,
                            height: 26,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: isDone
                                  ? const Color(0xFF064E3B)
                                  : isActive
                                      ? AppColors.blue
                                      : Colors.white.withOpacity(0.06),
                            ),
                            child: Center(
                              child: isDone
                                  ? const Icon(Icons.check,
                                      color: Color(0xFF34D399), size: 14)
                                  : isActive
                                      ? const SizedBox(
                                          width: 12,
                                          height: 12,
                                          child: CircularProgressIndicator(
                                            color: Colors.white,
                                            strokeWidth: 1.5,
                                          ),
                                        )
                                      : Text(
                                          "${idx + 1}",
                                          style: TextStyle(
                                            fontSize: 10,
                                            color: Colors.white
                                                .withOpacity(0.3),
                                          ),
                                        ),
                            ),
                          ),
                          const SizedBox(width: 12),
                          // Step name
                          Expanded(
                            child: Text(
                              step,
                              style: TextStyle(
                                fontSize: 13,
                                fontWeight: isActive
                                    ? FontWeight.w600
                                    : FontWeight.w400,
                                color: isDone || isActive
                                    ? Colors.white
                                    : Colors.white.withOpacity(0.4),
                              ),
                            ),
                          ),
                          // Done tick
                          if (isDone)
                            const Icon(Icons.check_circle,
                                color: Color(0xFF34D399), size: 14),
                        ]),
                      );
                    }).toList(),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
