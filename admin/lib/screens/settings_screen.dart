// =============================================================
// EduLink Admin — Settings Screen
// Profile (display name) editing via PATCH /admin/auth/me,
// password change via Firebase Auth (reauth + updatePassword).
// =============================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../models/admin_user.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';

class SettingsScreen extends StatefulWidget {
  final AdminUser admin;
  final ValueChanged<AdminUser> onAdminUpdated;

  const SettingsScreen({
    super.key,
    required this.admin,
    required this.onAdminUpdated,
  });

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late final TextEditingController _nameCtrl =
      TextEditingController(text: widget.admin.name);

  bool    _savingProfile  = false;
  String? _profileError;
  String? _profileSuccess;

  final _currentPassCtrl = TextEditingController();
  final _newPassCtrl     = TextEditingController();
  final _confirmPassCtrl = TextEditingController();
  bool    _obscure       = true;
  bool    _changingPass  = false;
  String? _passError;
  String? _passSuccess;

  bool get _nameChanged {
    final trimmed = _nameCtrl.text.trim();
    return trimmed.isNotEmpty && trimmed != widget.admin.name;
  }

  Future<void> _saveProfile() async {
    final name = _nameCtrl.text.trim();
    if (name.length < 2) {
      setState(() => _profileError = 'Name must be at least 2 characters.');
      return;
    }

    setState(() {
      _savingProfile  = true;
      _profileError   = null;
      _profileSuccess = null;
    });

    try {
      final updated = await ApiService.updateProfile(name: name);
      widget.onAdminUpdated(updated);
      if (!mounted) return;
      setState(() {
        _savingProfile  = false;
        _profileSuccess = 'Profile updated successfully.';
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _savingProfile = false;
        _profileError  = e.toString().replaceFirst('Exception: ', '');
      });
    }
  }

  Future<void> _changePassword() async {
    final current = _currentPassCtrl.text;
    final next    = _newPassCtrl.text;
    final confirm = _confirmPassCtrl.text;

    if (current.isEmpty) {
      setState(() => _passError = 'Enter your current password.');
      return;
    }
    if (next.length < 6) {
      setState(() => _passError = 'New password must be at least 6 characters.');
      return;
    }
    if (next != confirm) {
      setState(() => _passError = 'New password and confirmation do not match.');
      return;
    }

    setState(() {
      _changingPass = true;
      _passError    = null;
      _passSuccess  = null;
    });

    try {
      await AuthService.changePassword(
        currentPassword: current,
        newPassword:     next,
      );
      if (!mounted) return;
      _currentPassCtrl.clear();
      _newPassCtrl.clear();
      _confirmPassCtrl.clear();
      setState(() {
        _changingPass = false;
        _passSuccess  = 'Password updated successfully.';
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _changingPass = false;
        _passError    = e.toString().replaceFirst('Exception: ', '');
      });
    }
  }

  String _formatLastLogin(String iso) {
    try {
      final dt = DateTime.parse(iso).toLocal();
      const months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
      ];
      final hour12 = dt.hour % 12 == 0 ? 12 : dt.hour % 12;
      final ampm   = dt.hour < 12 ? 'AM' : 'PM';
      final minute = dt.minute.toString().padLeft(2, '0');
      return '${months[dt.month - 1]} ${dt.day}, ${dt.year} · $hour12:$minute $ampm';
    } catch (_) {
      return iso;
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Settings',
            style: GoogleFonts.plusJakartaSans(
              fontSize:   22,
              fontWeight: FontWeight.w700,
              color:      AppColors.text1,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            'Manage your admin account',
            style: GoogleFonts.plusJakartaSans(
              fontSize: 13,
              color:    AppColors.text3,
            ),
          ),
          const SizedBox(height: 24),

          LayoutBuilder(builder: (ctx, c) {
            final profile  = _profileCard();
            final security = _securityCard();
            if (c.maxWidth > 760) {
              return Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(child: profile),
                  const SizedBox(width: 16),
                  Expanded(child: security),
                ],
              );
            }
            return Column(children: [
              profile,
              const SizedBox(height: 16),
              security,
            ]);
          }),
        ],
      ),
    );
  }

  // ── Profile card ──────────────────────────────────────────
  Widget _profileCard() => _card(
        title: 'Profile',
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _readOnlyRow('Email', widget.admin.email),
            const SizedBox(height: 10),
            _readOnlyRow('Role', _titleCase(widget.admin.role)),
            if (widget.admin.lastLogin != null) ...[
              const SizedBox(height: 10),
              _readOnlyRow(
                  'Last sign-in', _formatLastLogin(widget.admin.lastLogin!)),
            ],
            const SizedBox(height: 18),
            _label('Display name'),
            const SizedBox(height: 5),
            TextField(
              controller: _nameCtrl,
              onChanged:  (_) => setState(() {}),
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 13, color: AppColors.text1),
              decoration: _inputDecoration(),
            ),
            const SizedBox(height: 14),
            if (_profileError != null)
              _banner(_profileError!, isError: true),
            if (_profileSuccess != null)
              _banner(_profileSuccess!, isError: false),
            if (_profileError != null || _profileSuccess != null)
              const SizedBox(height: 12),
            Align(
              alignment: Alignment.centerRight,
              child: ElevatedButton(
                onPressed: (_savingProfile || !_nameChanged)
                    ? null
                    : _saveProfile,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.sky,
                  foregroundColor: Colors.white,
                  disabledBackgroundColor: AppColors.border,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10)),
                  padding: const EdgeInsets.symmetric(
                      horizontal: 20, vertical: 12),
                ),
                child: _savingProfile
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(
                            color: Colors.white, strokeWidth: 2),
                      )
                    : Text(
                        'Save changes',
                        style: GoogleFonts.plusJakartaSans(
                            fontWeight: FontWeight.w600, fontSize: 13),
                      ),
              ),
            ),
          ],
        ),
      );

  // ── Security card ─────────────────────────────────────────
  Widget _securityCard() => _card(
        title: 'Change password',
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _passwordField('Current password', _currentPassCtrl),
            const SizedBox(height: 12),
            _passwordField('New password', _newPassCtrl),
            const SizedBox(height: 12),
            _passwordField('Confirm new password', _confirmPassCtrl),
            const SizedBox(height: 14),
            if (_passError != null) _banner(_passError!, isError: true),
            if (_passSuccess != null) _banner(_passSuccess!, isError: false),
            if (_passError != null || _passSuccess != null)
              const SizedBox(height: 12),
            Align(
              alignment: Alignment.centerRight,
              child: ElevatedButton(
                onPressed: _changingPass ? null : _changePassword,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.navy,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10)),
                  padding: const EdgeInsets.symmetric(
                      horizontal: 20, vertical: 12),
                ),
                child: _changingPass
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(
                            color: Colors.white, strokeWidth: 2),
                      )
                    : Text(
                        'Update password',
                        style: GoogleFonts.plusJakartaSans(
                            fontWeight: FontWeight.w600, fontSize: 13),
                      ),
              ),
            ),
          ],
        ),
      );

  // ── Shared building blocks ───────────────────────────────
  Widget _card({required String title, required Widget child}) => Container(
        width: double.infinity,
        decoration: BoxDecoration(
          color:        AppColors.card,
          borderRadius: BorderRadius.circular(14),
          border:       Border.all(color: AppColors.border),
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: GoogleFonts.plusJakartaSans(
                fontSize:   14,
                fontWeight: FontWeight.w700,
                color:      AppColors.text1,
              ),
            ),
            const SizedBox(height: 16),
            child,
          ],
        ),
      );

  Widget _readOnlyRow(String label, String value) => Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 90,
            child: Text(
              label,
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 12, color: AppColors.text3),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: GoogleFonts.plusJakartaSans(
                fontSize:   12,
                fontWeight: FontWeight.w600,
                color:      AppColors.text1,
              ),
            ),
          ),
        ],
      );

  Widget _label(String text) => Text(
        text,
        style: GoogleFonts.plusJakartaSans(
            fontSize: 11,
            fontWeight: FontWeight.w700,
            color: AppColors.text3,
            letterSpacing: .4),
      );

  Widget _passwordField(String label, TextEditingController ctrl) => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _label(label),
          const SizedBox(height: 5),
          TextField(
            controller:  ctrl,
            obscureText: _obscure,
            style: GoogleFonts.plusJakartaSans(
                fontSize: 13, color: AppColors.text1),
            decoration: _inputDecoration(hint: '••••••••').copyWith(
              suffixIcon: IconButton(
                icon: Icon(
                  _obscure
                      ? Icons.visibility_off_outlined
                      : Icons.visibility_outlined,
                  color: AppColors.text3,
                  size: 18,
                ),
                onPressed: () => setState(() => _obscure = !_obscure),
              ),
            ),
          ),
        ],
      );

  InputDecoration _inputDecoration({String hint = ''}) => InputDecoration(
        hintText:  hint,
        hintStyle: GoogleFonts.plusJakartaSans(
            fontSize: 13, color: AppColors.text3),
        filled:    true,
        fillColor: AppColors.surface,
        border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(10),
            borderSide: const BorderSide(color: AppColors.border)),
        enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(10),
            borderSide: const BorderSide(color: AppColors.border)),
        focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(10),
            borderSide:
                const BorderSide(color: AppColors.sky, width: 1.5)),
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      );

  Widget _banner(String message, {required bool isError}) => Container(
        margin:  const EdgeInsets.only(bottom: 4),
        width:   double.infinity,
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: isError ? AppColors.rosePale : AppColors.mintPale,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(
            color: (isError ? AppColors.rose : AppColors.mint)
                .withOpacity(.3),
          ),
        ),
        child: Text(
          message,
          style: GoogleFonts.plusJakartaSans(
            fontSize: 12,
            color: isError ? AppColors.rose : const Color(0xFF065F46),
          ),
        ),
      );

  String _titleCase(String s) =>
      s.isEmpty ? s : '${s[0].toUpperCase()}${s.substring(1)}';

  @override
  void dispose() {
    _nameCtrl.dispose();
    _currentPassCtrl.dispose();
    _newPassCtrl.dispose();
    _confirmPassCtrl.dispose();
    super.dispose();
  }
}
