import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../config/app_constants.dart';
import '../services/api_service.dart';
import 'writing_screen.dart';

class MCQScreen extends StatefulWidget {
  final String studentId;
  const MCQScreen({super.key, this.studentId = "STU001"});
  @override
  State<MCQScreen> createState() => _MCQScreenState();
}

class _MCQScreenState extends State<MCQScreen> {
  int _current = 0;
  final List<int> _answers = List.filled(40, 0);
  bool _loading = false;

  void _pick(int val) => setState(() => _answers[_current] = val);

  Future<void> _next() async {
    if (_answers[_current] == 0) _pick(3);
    if (_current < 39) {
      setState(() => _current++);
    } else {
      await _submit();
    }
  }

  void _back() {
    if (_current > 0) setState(() => _current--);
  }

  Future<void> _submit() async {
    setState(() => _loading = true);
    try {
      final Map<String, dynamic> data = {'student_id': widget.studentId};
      for (int i = 0; i < 40; i++) {
        data['Q${i + 1}'] = _answers[i] == 0 ? 3 : _answers[i];
      }

      final result = await ApiService.submitMCQ(data);

      if (result['status'] == 'error') {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Connection error: ${result['message']}'),
              backgroundColor: AppColors.rose,
              duration: const Duration(seconds: 3),
            ),
          );
        }
        return;
      }

      if (mounted)
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => WritingScreen(studentId: widget.studentId),
          ),
        );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: AppColors.rose),
        );
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final pct = (_current / 40 * 100).round();
    final section = AppConstants.getSectionForQuestion(_current);
    final question = AppConstants.questions[_current];

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Column(
        children: [
          // Header
          Container(
            color: AppColors.navy,
            padding: const EdgeInsets.fromLTRB(22, 52, 22, 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                GestureDetector(
                  onTap: _back,
                  child: Row(
                    children: [
                      const Icon(
                        Icons.arrow_back_ios,
                        color: Colors.white54,
                        size: 16,
                      ),
                      Text(
                        "Assessment",
                        style: TextStyle(color: Colors.white54, fontSize: 13),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      "Question ${_current + 1} of 40",
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    Text(
                      "$pct%",
                      style: TextStyle(
                        color: Colors.white.withOpacity(0.6),
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                ClipRRect(
                  borderRadius: BorderRadius.circular(2),
                  child: LinearProgressIndicator(
                    value: _current / 40,
                    backgroundColor: Colors.white.withOpacity(0.12),
                    valueColor: const AlwaysStoppedAnimation(Color(0xFF60A5FA)),
                    minHeight: 3,
                  ),
                ),
                const SizedBox(height: 10),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.08),
                    borderRadius: BorderRadius.circular(7),
                  ),
                  child: Text(
                    section,
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.6),
                      fontSize: 10,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                // Dot grid
                Wrap(
                  spacing: 3,
                  runSpacing: 3,
                  children: List.generate(
                    40,
                    (i) => Container(
                      width: 16,
                      height: 4,
                      decoration: BoxDecoration(
                        color: i == _current
                            ? Colors.white
                            : _answers[i] > 0
                            ? const Color(0xFF60A5FA)
                            : Colors.white.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(2),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          // Question card
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: AppColors.card,
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "QUESTION ${_current + 1}",
                          style: const TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w700,
                            color: AppColors.blue,
                            letterSpacing: 0.6,
                          ),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          '"$question"',
                          style: const TextStyle(
                            fontSize: 15,
                            color: AppColors.text1,
                            height: 1.6,
                          ),
                        ),
                        const SizedBox(height: 20),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Strongly disagree",
                              style: TextStyle(
                                fontSize: 9,
                                color: AppColors.text3,
                              ),
                            ),
                            Text(
                              "Strongly agree",
                              style: TextStyle(
                                fontSize: 9,
                                color: AppColors.text3,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        Row(
                          children: List.generate(5, (i) {
                            final val = i + 1;
                            final selected = _answers[_current] == val;
                            return Expanded(
                              child: GestureDetector(
                                onTap: () => _pick(val),
                                child: AnimatedContainer(
                                  duration: const Duration(milliseconds: 150),
                                  margin: const EdgeInsets.symmetric(
                                    horizontal: 3,
                                  ),
                                  height: 46,
                                  decoration: BoxDecoration(
                                    color: selected
                                        ? AppColors.navy
                                        : AppColors.surface,
                                    borderRadius: BorderRadius.circular(10),
                                    border: Border.all(
                                      color: selected
                                          ? AppColors.navy
                                          : AppColors.border,
                                      width: selected ? 1.5 : 1,
                                    ),
                                  ),
                                  child: Center(
                                    child: Text(
                                      "$val",
                                      style: TextStyle(
                                        fontSize: 15,
                                        fontWeight: FontWeight.w700,
                                        color: selected
                                            ? Colors.white
                                            : AppColors.text2,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            );
                          }),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          // Navigation
          Container(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 20),
            color: AppColors.card,
            child: Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: _back,
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      side: const BorderSide(color: AppColors.border),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: const Text(
                      "← Back",
                      style: TextStyle(color: AppColors.text2),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  flex: 2,
                  child: ElevatedButton(
                    onPressed: _loading ? null : _next,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.navy,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: _loading
                        ? const CircularProgressIndicator(
                            color: Colors.white,
                            strokeWidth: 2,
                          )
                        : Text(
                            _current == 39 ? "Finish ✓" : "Next →",
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
        ],
      ),
    );
  }
}
