import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';
import '../models/student_model.dart';
import 'package:uuid/uuid.dart';
import 'mcq_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});
  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  // Controllers
  final _firstNameCtrl = TextEditingController();
  final _lastNameCtrl = TextEditingController();
  final _ageCtrl = TextEditingController();
  final _schoolCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  final _confirmCtrl = TextEditingController();

  String _grade = 'AL';
  String _stream = 'Technology';
  String _gender = '';
  String? _district;
  bool _loading = false;
  bool _showPass = false;
  bool _showConfirm = false;
  String? _error;

  // ── 25 Sri Lanka districts ────────────────────────────────
  static const List<String> _districts = [
    'Ampara',
    'Anuradhapura',
    'Badulla',
    'Batticaloa',
    'Colombo',
    'Galle',
    'Gampaha',
    'Hambantota',
    'Jaffna',
    'Kalutara',
    'Kandy',
    'Kegalle',
    'Kilinochchi',
    'Kurunegala',
    'Mannar',
    'Matale',
    'Matara',
    'Monaragala',
    'Mullaitivu',
    'Nuwara Eliya',
    'Polonnaruwa',
    'Puttalam',
    'Ratnapura',
    'Trincomalee',
    'Vavuniya',
  ];

  static const List<String> _streams = [
    'Technology',
    'Science',
    'Commerce',
    'Arts',
    'Mathematics',
  ];

  // ── Validation ────────────────────────────────────────────
  String? _validate() {
    if (_firstNameCtrl.text.trim().length < 2)
      return "First name must be at least 2 characters";
    if (_lastNameCtrl.text.trim().length < 2)
      return "Last name must be at least 2 characters";
    final age = int.tryParse(_ageCtrl.text.trim());
    if (age == null) return "Please enter a valid age";
    if (age < 10 || age > 25) return "Age must be between 10 and 25";
    if (_gender.isEmpty) return "Please select your gender";
    if (_schoolCtrl.text.trim().length < 2)
      return "Please enter your school name";
    if (_district == null) return "Please select your district";
    final email = _emailCtrl.text.trim();
    if (email.isEmpty || !email.contains('@'))
      return "Please enter a valid email address";
    if (_passCtrl.text.length < 6)
      return "Password must be at least 6 characters";
    if (_passCtrl.text != _confirmCtrl.text) return "Passwords do not match";
    if (_grade == 'AL' && _stream.isEmpty) return "Please select your stream";
    return null;
  }

  // ── Register ──────────────────────────────────────────────
  Future<void> _register() async {
    final err = _validate();
    if (err != null) {
      setState(() => _error = err);
      return;
    }

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      await AuthService.register(_emailCtrl.text.trim(), _passCtrl.text);
      final studentId = const Uuid().v4().substring(0, 8).toUpperCase();
      final fullName =
          '${_firstNameCtrl.text.trim()} ${_lastNameCtrl.text.trim()}';

      final student = StudentModel(
        studentId: studentId,
        name: fullName,
        age: int.parse(_ageCtrl.text.trim()),
        grade: _grade,
        stream: _grade == 'OL' ? 'N/A' : _stream,
        school: _schoolCtrl.text.trim(),
        district: _district!,
      );
      await ApiService.registerStudent(student.toJson());

      if (mounted)
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => MCQScreen(studentId: studentId)),
        );
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      setState(() => _loading = false);
    }
  }

  // ── Build ─────────────────────────────────────────────────
  @override
  Widget build(BuildContext context) {
    final passMatch =
        _confirmCtrl.text.isNotEmpty && _passCtrl.text == _confirmCtrl.text;
    final passMismatch =
        _confirmCtrl.text.isNotEmpty && _passCtrl.text != _confirmCtrl.text;

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Column(
        children: [
          // ── Header ───────────────────────────────────────────
          Container(
            color: AppColors.navy,
            padding: const EdgeInsets.fromLTRB(24, 60, 24, 24),
            width: double.infinity,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                GestureDetector(
                  onTap: () => Navigator.pop(context),
                  child: const Row(
                    children: [
                      Icon(
                        Icons.arrow_back_ios,
                        color: Colors.white54,
                        size: 16,
                      ),
                      Text(
                        "Back",
                        style: TextStyle(color: Colors.white54, fontSize: 13),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
                Text(
                  "Create account",
                  style: GoogleFonts.playfairDisplay(
                    fontSize: 28,
                    color: Colors.white,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                Text(
                  "Tell us about yourself",
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.white.withOpacity(0.5),
                  ),
                ),
              ],
            ),
          ),

          // ── Form ─────────────────────────────────────────────
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // First + Last name
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            _label("First name"),
                            _input(_firstNameCtrl, "Kasun"),
                          ],
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            _label("Last name"),
                            _input(_lastNameCtrl, "Perera"),
                          ],
                        ),
                      ),
                    ],
                  ),

                  // Age + Gender
                  _label("Age"),
                  _input(_ageCtrl, "17", type: TextInputType.number),

                  // Gender
                  _label("Gender"),
                  _genderSelector(),

                  // School
                  _label("School"),
                  _input(_schoolCtrl, "Nalanda College, Colombo"),

                  // District dropdown
                  _label("District"),
                  _districtDropdown(),

                  // Grade
                  _label("Grade"),
                  _chips(['AL', 'OL'], _grade, (v) {
                    setState(() {
                      _grade = v;
                      if (v == 'OL') _stream = '';
                    });
                  }),
                  const SizedBox(height: 10),

                  // Stream — hidden when OL selected
                  if (_grade == 'AL') ...[
                    _label("Stream"),
                    _chips(
                      _streams,
                      _stream,
                      (v) => setState(() => _stream = v),
                    ),
                    const SizedBox(height: 10),
                  ],

                  // OL notice
                  if (_grade == 'OL') ...[
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 10,
                      ),
                      decoration: BoxDecoration(
                        color: AppColors.goldPale,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                          color: AppColors.gold.withOpacity(0.3),
                        ),
                      ),
                      child: Row(
                        children: [
                          const Icon(
                            Icons.info_outline,
                            color: AppColors.gold,
                            size: 16,
                          ),
                          const SizedBox(width: 8),
                          const Expanded(
                            child: Text(
                              "Stream selection is not required for O/L students.",
                              style: TextStyle(
                                fontSize: 11,
                                color: AppColors.text2,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 10),
                  ],

                  // Email
                  _label("Email"),
                  _input(
                    _emailCtrl,
                    "kasun@email.com",
                    type: TextInputType.emailAddress,
                  ),

                  // Password
                  _label("Password"),
                  _passwordField(
                    ctrl: _passCtrl,
                    hint: "Create a password",
                    show: _showPass,
                    onToggle: () => setState(() => _showPass = !_showPass),
                  ),

                  // Confirm password
                  _label("Confirm password"),
                  _passwordField(
                    ctrl: _confirmCtrl,
                    hint: "Re-enter password",
                    show: _showConfirm,
                    onToggle: () =>
                        setState(() => _showConfirm = !_showConfirm),
                    suffix: _confirmCtrl.text.isEmpty
                        ? null
                        : Icon(
                            passMatch ? Icons.check_circle : Icons.cancel,
                            color: passMatch ? AppColors.mint : AppColors.rose,
                            size: 18,
                          ),
                  ),

                  // Password match message
                  if (passMatch || passMismatch) ...[
                    const SizedBox(height: 6),
                    Row(
                      children: [
                        Icon(
                          passMatch ? Icons.check_circle : Icons.cancel,
                          size: 13,
                          color: passMatch ? AppColors.mint : AppColors.rose,
                        ),
                        const SizedBox(width: 5),
                        Text(
                          passMatch
                              ? "Passwords match"
                              : "Passwords do not match",
                          style: TextStyle(
                            fontSize: 11,
                            color: passMatch ? AppColors.mint : AppColors.rose,
                          ),
                        ),
                      ],
                    ),
                  ],

                  // Error box
                  if (_error != null) ...[
                    const SizedBox(height: 10),
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: AppColors.rosePale,
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Row(
                        children: [
                          const Icon(
                            Icons.error_outline,
                            color: AppColors.rose,
                            size: 16,
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              _error!,
                              style: const TextStyle(
                                color: AppColors.rose,
                                fontSize: 12,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],

                  const SizedBox(height: 20),

                  // Submit
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _loading ? null : _register,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.navy,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(14),
                        ),
                      ),
                      child: _loading
                          ? const CircularProgressIndicator(
                              color: Colors.white,
                              strokeWidth: 2,
                            )
                          : Text(
                              "Continue to assessment →",
                              style: GoogleFonts.plusJakartaSans(
                                fontSize: 15,
                                fontWeight: FontWeight.w600,
                                color: Colors.white,
                              ),
                            ),
                    ),
                  ),

                  const SizedBox(height: 12),
                  const Center(
                    child: Text(
                      "Your data is kept private and anonymous",
                      style: TextStyle(fontSize: 11, color: AppColors.text3),
                    ),
                  ),
                  const SizedBox(height: 20),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ── Gender selector ───────────────────────────────────────
  Widget _genderSelector() => Row(
    children: [
      _genderChip('Male', Icons.male),
      const SizedBox(width: 8),
      _genderChip('Female', Icons.female),
      const SizedBox(width: 8),
      _genderChip('Other', Icons.person_outline),
    ],
  );

  Widget _genderChip(String value, IconData icon) {
    final selected = _gender == value;
    return Expanded(
      child: GestureDetector(
        onTap: () => setState(() {
          _gender = value;
          _error = null;
        }),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(
            color: selected ? AppColors.navy : AppColors.card,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(
              color: selected ? AppColors.navy : AppColors.border,
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                size: 18,
                color: selected ? Colors.white : AppColors.text2,
              ),
              const SizedBox(height: 3),
              Text(
                value,
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.w500,
                  color: selected ? Colors.white : AppColors.text2,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // ── District dropdown ─────────────────────────────────────
  Widget _districtDropdown() => Container(
    padding: const EdgeInsets.symmetric(horizontal: 14),
    decoration: BoxDecoration(
      color: AppColors.card,
      borderRadius: BorderRadius.circular(12),
      border: Border.all(color: AppColors.border),
    ),
    child: DropdownButtonHideUnderline(
      child: DropdownButton<String>(
        value: _district,
        hint: const Text(
          "Select your district",
          style: TextStyle(color: AppColors.text3, fontSize: 13),
        ),
        isExpanded: true,
        icon: const Icon(
          Icons.keyboard_arrow_down,
          color: AppColors.text3,
          size: 20,
        ),
        items: _districts
            .map(
              (d) => DropdownMenuItem(
                value: d,
                child: Text(
                  d,
                  style: const TextStyle(fontSize: 13, color: AppColors.text1),
                ),
              ),
            )
            .toList(),
        onChanged: (v) => setState(() {
          _district = v;
          _error = null;
        }),
      ),
    ),
  );

  // ── Password field with show/hide and optional suffix ─────
  Widget _passwordField({
    required TextEditingController ctrl,
    required String hint,
    required bool show,
    required VoidCallback onToggle,
    Widget? suffix,
  }) => TextField(
    controller: ctrl,
    obscureText: !show,
    onChanged: (_) => setState(() => _error = null),
    decoration: InputDecoration(
      hintText: hint,
      hintStyle: const TextStyle(color: AppColors.text3),
      filled: true,
      fillColor: AppColors.card,
      suffixIcon: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (suffix != null)
            Padding(padding: const EdgeInsets.only(right: 4), child: suffix),
          IconButton(
            icon: Icon(
              show ? Icons.visibility_off : Icons.visibility,
              color: AppColors.text3,
              size: 18,
            ),
            onPressed: onToggle,
          ),
        ],
      ),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.border),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.border),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.blue, width: 1.5),
      ),
      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 13),
    ),
  );

  // ── Helpers ───────────────────────────────────────────────
  Widget _label(String text) => Padding(
    padding: const EdgeInsets.only(bottom: 5, top: 12),
    child: Text(
      text.toUpperCase(),
      style: const TextStyle(
        fontSize: 10,
        fontWeight: FontWeight.w600,
        color: AppColors.text2,
        letterSpacing: 0.5,
      ),
    ),
  );

  Widget _input(
    TextEditingController ctrl,
    String hint, {
    TextInputType type = TextInputType.text,
  }) => TextField(
    controller: ctrl,
    keyboardType: type,
    onChanged: (_) => setState(() => _error = null),
    decoration: InputDecoration(
      hintText: hint,
      hintStyle: const TextStyle(color: AppColors.text3),
      filled: true,
      fillColor: AppColors.card,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.border),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.border),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.blue, width: 1.5),
      ),
      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 13),
    ),
  );

  Widget _chips(
    List<String> options,
    String selected,
    Function(String) onTap,
  ) => Wrap(
    spacing: 8,
    runSpacing: 8,
    children: options
        .map(
          (o) => GestureDetector(
            onTap: () => onTap(o),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              decoration: BoxDecoration(
                color: selected == o ? AppColors.navy : AppColors.card,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(
                  color: selected == o ? AppColors.navy : AppColors.border,
                ),
              ),
              child: Text(
                o,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w500,
                  color: selected == o ? Colors.white : AppColors.text2,
                ),
              ),
            ),
          ),
        )
        .toList(),
  );
}
