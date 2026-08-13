import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../config/app_colors.dart';
import '../services/auth_service.dart';
import 'login_screen.dart';
import 'mcq_screen.dart';
import 'dashboard_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});
  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _navigate();
  }

  Future<void> _navigate() async {
    await Future.delayed(const Duration(seconds: 3));
    if (!mounted) return;

    final user = FirebaseAuth.instance.currentUser;

    if (user == null) {
      // Not logged in → LoginScreen
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const LoginScreen()),
      );
      return;
    }

    // Logged in — restore session
    try {
      final studentId = await AuthService.getStudentId();

      if (studentId == null) {
        // No mapping found → LoginScreen
        await AuthService.signOut();
        if (mounted)
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (_) => const LoginScreen()),
          );
        return;
      }

      final hasHistory =
          await AuthService.hasAssessmentHistory(studentId);

      if (mounted) {
        if (hasHistory) {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (_) => DashboardScreen(studentId: studentId),
            ),
          );
        } else {
          final assessmentId =
              AuthService.generateAssessmentId(studentId);
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (_) => MCQScreen(
                studentId: studentId,
                assessmentId: assessmentId,
              ),
            ),
          );
        }
      }
    } catch (e) {
      if (mounted)
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const LoginScreen()),
        );
    }
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      backgroundColor: AppColors.navy,
      body: SizedBox(
        width: double.infinity,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Spacer(),
            Container(
              width: 120,
              height: 120,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(30),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.3),
                    blurRadius: 20,
                    offset: const Offset(0, 8),
                  ),
                ],
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(30),
                child: Image.asset(
                  'assets/images/logo.jpeg',
                  width: 120,
                  height: 120,
                  fit: BoxFit.cover,
                ),
              ),
            ),
            const SizedBox(height: 28),
            Text(
              "EduLink",
              textAlign: TextAlign.center,
              style: GoogleFonts.playfairDisplay(
                fontSize: 42,
                fontWeight: FontWeight.w700,
                color: Colors.white,
                letterSpacing: 2,
              ),
            ),
            const SizedBox(height: 12),
            Padding(
              padding:
                  EdgeInsets.symmetric(horizontal: screenWidth * 0.1),
              child: Text(
                "AI-driven career guidance\nfor Sri Lankan IT students",
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 15,
                  color: Colors.white.withOpacity(0.6),
                  height: 1.6,
                  letterSpacing: 0.3,
                ),
              ),
            ),
            const Spacer(),
            SizedBox(
              width: 24,
              height: 24,
              child: CircularProgressIndicator(
                color: Colors.white.withOpacity(0.5),
                strokeWidth: 2,
              ),
            ),
            const SizedBox(height: 32),
            Text(
              "v2.0.0",
              style: TextStyle(
                fontSize: 11,
                color: Colors.white.withOpacity(0.3),
                letterSpacing: 1,
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}
