// =============================================================
// EduLink Admin — Login Screen
// =============================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../services/auth_service.dart';
import '../models/admin_user.dart';

class LoginScreen extends StatefulWidget {
  final ValueChanged<AdminUser> onLogin;
  const LoginScreen({super.key, required this.onLogin});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailCtrl = TextEditingController();
  final _passCtrl  = TextEditingController();
  bool   _loading  = false;
  bool   _obscure  = true;
  String? _error;

  Future<void> _signIn() async {
    final email    = _emailCtrl.text.trim();
    final password = _passCtrl.text;

    if (email.isEmpty || !email.contains('@')) {
      setState(() => _error = 'Enter a valid email address.');
      return;
    }
    if (password.isEmpty) {
      setState(() => _error = 'Password is required.');
      return;
    }

    setState(() { _loading = true; _error = null; });

    try {
      final admin = await AuthService.signIn(email, password);
      widget.onLogin(admin);
    } catch (e) {
      setState(() => _error = e.toString().replaceFirst('Exception: ', ''));
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.navy,
      body: Center(
        child: SingleChildScrollView(
          child: Container(
            width: 420,
            margin: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color:        AppColors.card,
              borderRadius: BorderRadius.circular(20),
              border:       Border.all(color: AppColors.border),
            ),
            padding: const EdgeInsets.all(36),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Logo
                Container(
                  width: 64,
                  height: 64,
                  decoration: BoxDecoration(
                    color:        AppColors.navy,
                    borderRadius: BorderRadius.circular(18),
                  ),
                  child: const Icon(Icons.school,
                      color: Colors.white, size: 32),
                ),
                const SizedBox(height: 16),
                Text(
                  'EduLink Admin',
                  style: GoogleFonts.plusJakartaSans(
                    fontSize: 22,
                    fontWeight: FontWeight.w700,
                    color: AppColors.text1,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  'Sign in to manage the education knowledge base',
                  style: GoogleFonts.plusJakartaSans(
                    fontSize: 13,
                    color: AppColors.text3,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 32),

                // Error banner
                if (_error != null) ...[
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color:        AppColors.rosePale,
                      borderRadius: BorderRadius.circular(10),
                      border:       Border.all(color: AppColors.rose.withOpacity(.3)),
                    ),
                    child: Text(
                      _error!,
                      style: GoogleFonts.plusJakartaSans(
                          fontSize: 13, color: AppColors.rose),
                    ),
                  ),
                  const SizedBox(height: 16),
                ],

                // Email
                _field(
                  controller: _emailCtrl,
                  label:       'Email address',
                  hint:        'admin@edulink.lk',
                  keyboard:    TextInputType.emailAddress,
                ),
                const SizedBox(height: 12),

                // Password
                TextField(
                  controller:    _passCtrl,
                  obscureText:   _obscure,
                  onSubmitted:   (_) => _signIn(),
                  style: GoogleFonts.plusJakartaSans(
                      fontSize: 14, color: AppColors.text1),
                  decoration: InputDecoration(
                    labelText:    'Password',
                    hintText:     '••••••••',
                    labelStyle:   GoogleFonts.plusJakartaSans(
                        fontSize: 12,
                        fontWeight: FontWeight.w700,
                        color: AppColors.text3,
                        letterSpacing: .4),
                    filled:       true,
                    fillColor:    AppColors.surface,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide:   const BorderSide(color: AppColors.border),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide:   const BorderSide(color: AppColors.border),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide:   const BorderSide(color: AppColors.sky, width: 1.5),
                    ),
                    suffixIcon: IconButton(
                      icon: Icon(
                        _obscure
                            ? Icons.visibility_off_outlined
                            : Icons.visibility_outlined,
                        color: AppColors.text3,
                        size: 18,
                      ),
                      onPressed: () =>
                          setState(() => _obscure = !_obscure),
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                // Sign in button
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _loading ? null : _signIn,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.navy,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12)),
                    ),
                    child: _loading
                        ? const SizedBox(
                            width: 18,
                            height: 18,
                            child: CircularProgressIndicator(
                                color: Colors.white, strokeWidth: 2),
                          )
                        : Text(
                            'Sign in',
                            style: GoogleFonts.plusJakartaSans(
                              fontSize: 15,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                  ),
                ),

                const SizedBox(height: 16),
                Text(
                  'Admin accounts are managed by the system administrator.',
                  style: GoogleFonts.plusJakartaSans(
                      fontSize: 11, color: AppColors.text3),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _field({
    required TextEditingController controller,
    required String label,
    required String hint,
    TextInputType keyboard = TextInputType.text,
  }) =>
      TextField(
        controller:  controller,
        keyboardType: keyboard,
        style: GoogleFonts.plusJakartaSans(
            fontSize: 14, color: AppColors.text1),
        decoration: InputDecoration(
          labelText:  label,
          hintText:   hint,
          labelStyle: GoogleFonts.plusJakartaSans(
              fontSize: 12,
              fontWeight: FontWeight.w700,
              color: AppColors.text3,
              letterSpacing: .4),
          filled:     true,
          fillColor:  AppColors.surface,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide:   const BorderSide(color: AppColors.border),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide:   const BorderSide(color: AppColors.border),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide:   const BorderSide(color: AppColors.sky, width: 1.5),
          ),
        ),
      );

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passCtrl.dispose();
    super.dispose();
  }
}
