// =============================================================
// EduLink Admin — Program Add/Edit Form
// 7 collapsible sections
// =============================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../models/university.dart';
import '../models/degree_program.dart';
import '../services/api_service.dart';

class ProgramFormScreen extends StatefulWidget {
  final University university;
  final DegreeProgram? program; // null = create
  const ProgramFormScreen({
    super.key,
    required this.university,
    this.program,
  });

  @override
  State<ProgramFormScreen> createState() => _ProgramFormScreenState();
}

class _ProgramFormScreenState extends State<ProgramFormScreen> {
  // Section open/close state
  final _open = List.filled(7, false)..[0] = true; // Section 1 open by default

  // Controllers
  final _degreeNameCtrl = TextEditingController();
  final _facultyCtrl = TextEditingController();
  final _shortDescCtrl = TextEditingController();
  final _fullDescCtrl = TextEditingController();
  final _durationCtrl = TextEditingController();
  final _mediumCtrl = TextEditingController();
  final _qualificationCtrl = TextEditingController();
  final _entryReqCtrl = TextEditingController();
  final _tuitionFeeCtrl = TextEditingController();
  final _regFeeCtrl = TextEditingController();
  final _campusNameCtrl = TextEditingController();
  final _addressCtrl = TextEditingController();
  final _latCtrl = TextEditingController();
  final _lngCtrl = TextEditingController();
  final _nextIntakeCtrl = TextEditingController();
  final _deadlineCtrl = TextEditingController();
  final _phoneCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _websiteCtrl = TextEditingController();
  final _degreePageCtrl = TextEditingController();
  final _applyNowCtrl = TextEditingController();
  final _accreditationCtrl = TextEditingController();
  final _scholarshipsCtrl = TextEditingController();
  final _financialAidCtrl = TextEditingController();
  final _paymentPlansCtrl = TextEditingController();
  final _logoUrlCtrl = TextEditingController();
  final _campusImageCtrl = TextEditingController();
  final _virtualTourCtrl = TextEditingController();
  final _brochureCtrl = TextEditingController();

  // Dropdown values
  String _studyMode = 'Full-time';
  String _feeType = 'Free';
  String _currency = 'LKR';
  String _applicationStatus = 'Coming Soon';
  String _status = 'Active';
  bool _installment = false;
  bool _ugcRecognized = false;
  bool _ministryRecognized = false;

  bool _loading = false;
  String? _error;

  bool get _isEdit => widget.program != null;

  @override
  void initState() {
    super.initState();
    if (_isEdit) _populate(widget.program!);
  }

  void _populate(DegreeProgram p) {
    _degreeNameCtrl.text = p.degreeName;
    _facultyCtrl.text = p.faculty;
    _shortDescCtrl.text = p.shortDescription;
    _fullDescCtrl.text = p.fullDescription;
    _durationCtrl.text = p.duration;
    _mediumCtrl.text = p.medium;
    _qualificationCtrl.text = p.qualification;
    _entryReqCtrl.text = p.entryRequirements;
    _tuitionFeeCtrl.text =
        p.tuitionFee > 0 ? p.tuitionFee.toStringAsFixed(0) : '';
    _regFeeCtrl.text =
        p.registrationFee > 0 ? p.registrationFee.toStringAsFixed(0) : '';
    _campusNameCtrl.text = p.campusName;
    _addressCtrl.text = p.address;
    _latCtrl.text = p.latitude?.toString() ?? '';
    _lngCtrl.text = p.longitude?.toString() ?? '';
    _nextIntakeCtrl.text = p.nextIntake;
    _deadlineCtrl.text = p.applicationDeadline;
    _phoneCtrl.text = p.phone;
    _emailCtrl.text = p.email;
    _websiteCtrl.text = p.officialWebsite;
    _degreePageCtrl.text = p.degreePageUrl;
    _applyNowCtrl.text = p.applyNowUrl;
    _accreditationCtrl.text = p.accreditation;
    _scholarshipsCtrl.text = p.scholarships;
    _financialAidCtrl.text = p.financialAid;
    _paymentPlansCtrl.text = p.paymentPlans;
    _logoUrlCtrl.text = p.logoUrl;
    _campusImageCtrl.text = p.campusImageUrl;
    _virtualTourCtrl.text = p.virtualTourUrl;
    _brochureCtrl.text = p.brochureUrl;
    _studyMode = p.studyMode;
    _feeType = p.feeType;
    _currency = p.currency;
    _applicationStatus = p.applicationStatus;
    _status = p.status;
    _installment = p.installmentAvailable;
    _ugcRecognized = p.ugcRecognized;
    _ministryRecognized = p.ministryRecognized;
  }

  Future<void> _save() async {
    if (_degreeNameCtrl.text.trim().isEmpty) {
      setState(() => _error = 'Degree name is required.');
      return;
    }
    if (_facultyCtrl.text.trim().isEmpty) {
      setState(() => _error = 'Faculty is required.');
      return;
    }

    setState(() {
      _loading = true;
      _error = null;
    });

    final data = <String, dynamic>{
      'universityId': widget.university.id,
      'universityName': widget.university.name,
      'degreeName': _degreeNameCtrl.text.trim(),
      'faculty': _facultyCtrl.text.trim(),
      'shortDescription': _shortDescCtrl.text.trim(),
      'fullDescription': _fullDescCtrl.text.trim(),
      'duration': _durationCtrl.text.trim(),
      'studyMode': _studyMode,
      'medium': _mediumCtrl.text.trim(),
      'qualification': _qualificationCtrl.text.trim(),
      'entryRequirements': _entryReqCtrl.text.trim(),
      'feeType': _feeType,
      'tuitionFee': double.tryParse(_tuitionFeeCtrl.text) ?? 0,
      'currency': _currency,
      'registrationFee': double.tryParse(_regFeeCtrl.text) ?? 0,
      'installmentAvailable': _installment,
      'campusName': _campusNameCtrl.text.trim(),
      'address': _addressCtrl.text.trim(),
      'latitude': double.tryParse(_latCtrl.text),
      'longitude': double.tryParse(_lngCtrl.text),
      'nextIntake': _nextIntakeCtrl.text.trim(),
      'applicationStatus': _applicationStatus,
      'applicationDeadline': _deadlineCtrl.text.trim(),
      'phone': _phoneCtrl.text.trim(),
      'email': _emailCtrl.text.trim(),
      'officialWebsite': _websiteCtrl.text.trim(),
      'degreePageUrl': _degreePageCtrl.text.trim(),
      'applyNowUrl': _applyNowCtrl.text.trim(),
      'ugcRecognized': _ugcRecognized,
      'ministryRecognized': _ministryRecognized,
      'accreditation': _accreditationCtrl.text.trim(),
      'scholarships': _scholarshipsCtrl.text.trim(),
      'financialAid': _financialAidCtrl.text.trim(),
      'paymentPlans': _paymentPlansCtrl.text.trim(),
      'logoUrl': _logoUrlCtrl.text.trim(),
      'campusImageUrl': _campusImageCtrl.text.trim(),
      'virtualTourUrl': _virtualTourCtrl.text.trim(),
      'brochureUrl': _brochureCtrl.text.trim(),
      'status': _status,
    };
    // Remove null lat/lng
    data.removeWhere(
        (k, v) => (k == 'latitude' || k == 'longitude') && v == null);

    try {
      if (_isEdit) {
        await ApiService.updateProgram(widget.program!.id, data);
      } else {
        await ApiService.createProgram(data);
      }
      if (mounted) Navigator.pop(context, true);
    } catch (e) {
      setState(() {
        _error = e.toString().replaceFirst('Exception: ', '');
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        backgroundColor: AppColors.navy,
        foregroundColor: Colors.white,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              _isEdit ? 'Edit program' : 'Add degree program',
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 15,
                  fontWeight: FontWeight.w700,
                  color: Colors.white),
            ),
            Text(
              widget.university.name,
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 11, color: const Color(0xFF6B87C4)),
            ),
          ],
        ),
        actions: [
          if (_loading)
            const Padding(
              padding: EdgeInsets.all(14),
              child: SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(
                      color: Colors.white, strokeWidth: 2)),
            )
          else
            TextButton(
              onPressed: _save,
              child: Text(
                _isEdit ? 'Save changes' : 'Save program',
                style: GoogleFonts.plusJakartaSans(
                    color: Colors.white, fontWeight: FontWeight.w600),
              ),
            ),
        ],
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 760),
            child: Column(
              children: [
                if (_error != null) ...[
                  _errorBanner(),
                  const SizedBox(height: 12),
                ],
                _section(0, 'Basic information', _basicSection()),
                _section(1, 'Academic details', _academicSection()),
                _section(2, 'Admission and fees', _feesSection()),
                _section(3, 'Campus and location', _campusSection()),
                _section(4, 'Intake and contact', _intakeSection()),
                _section(
                    5, 'Recognition and scholarships', _recognitionSection()),
                _section(6, 'Resources and images', _resourcesSection()),
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    OutlinedButton(
                      onPressed: () => Navigator.pop(context),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppColors.text2,
                        side: const BorderSide(color: AppColors.border),
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10)),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 20, vertical: 13),
                      ),
                      child: const Text('Cancel'),
                    ),
                    const SizedBox(width: 12),
                    ElevatedButton(
                      onPressed: _loading ? null : _save,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.sky,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10)),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 24, vertical: 13),
                      ),
                      child: Text(
                        _isEdit ? 'Save changes' : 'Save program',
                        style: GoogleFonts.plusJakartaSans(
                            fontWeight: FontWeight.w600),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // ── Collapsible section wrapper ──────────────────────────
  Widget _section(int idx, String title, Widget body) {
    final open = _open[idx];
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        children: [
          InkWell(
            onTap: () => setState(() => _open[idx] = !open),
            borderRadius: open
                ? const BorderRadius.only(
                    topLeft: Radius.circular(14),
                    topRight: Radius.circular(14),
                  )
                : BorderRadius.circular(14),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              child: Row(
                children: [
                  Container(
                    width: 22,
                    height: 22,
                    decoration: BoxDecoration(
                      color: open ? AppColors.mintPale : AppColors.surface,
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: open ? AppColors.mint : AppColors.border,
                      ),
                    ),
                    child: Icon(
                      open ? Icons.check : Icons.more_horiz,
                      size: 12,
                      color: open ? const Color(0xFF065F46) : AppColors.text3,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Text(
                    title,
                    style: GoogleFonts.plusJakartaSans(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: AppColors.text1),
                  ),
                  const Spacer(),
                  Icon(
                    open ? Icons.keyboard_arrow_up : Icons.keyboard_arrow_down,
                    color: AppColors.text3,
                    size: 18,
                  ),
                ],
              ),
            ),
          ),
          if (open)
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
              child: body,
            ),
        ],
      ),
    );
  }

  // ── Section bodies ────────────────────────────────────────

  Widget _basicSection() => Column(children: [
        _f('Degree name *', _degreeNameCtrl,
            hint: 'BSc (Hons) in Computer Science'),
        const SizedBox(height: 10),
        _row2(_f('Faculty *', _facultyCtrl, hint: 'Faculty of Engineering'),
            _f('Qualification', _qualificationCtrl, hint: 'BSc (Hons)')),
        const SizedBox(height: 10),
        _f('Short description', _shortDescCtrl,
            hint: 'One-line summary', maxLines: 2),
        const SizedBox(height: 10),
        _f('Full description', _fullDescCtrl,
            hint: 'Detailed program information', maxLines: 5),
      ]);

  Widget _academicSection() => Column(children: [
        _row2(
          _f('Duration', _durationCtrl, hint: '4 Years'),
          _dd(
              'Study mode',
              _studyMode,
              ['Full-time', 'Part-time', 'Online', 'Mixed'],
              (v) => setState(() => _studyMode = v!)),
        ),
        const SizedBox(height: 10),
        _row2(
          _f('Medium of instruction', _mediumCtrl, hint: 'English'),
          _dd('Status', _status, ['Active', 'Inactive'],
              (v) => setState(() => _status = v!)),
        ),
      ]);

  Widget _feesSection() => Column(children: [
        _row2(
          _dd('Fee type *', _feeType, ['Free', 'Paid'],
              (v) => setState(() => _feeType = v!)),
          _dd('Currency', _currency, ['LKR', 'USD'],
              (v) => setState(() => _currency = v!)),
        ),
        if (_feeType == 'Paid') ...[
          const SizedBox(height: 10),
          _row2(
            _f('Tuition fee', _tuitionFeeCtrl,
                hint: '375000', keyboard: TextInputType.number),
            _f('Registration fee', _regFeeCtrl,
                hint: '25000', keyboard: TextInputType.number),
          ),
          const SizedBox(height: 8),
          CheckboxListTile(
            value: _installment,
            onChanged: (v) => setState(() => _installment = v!),
            title: Text('Installment payment available',
                style: GoogleFonts.plusJakartaSans(
                    fontSize: 13, color: AppColors.text1)),
            activeColor: AppColors.sky,
            controlAffinity: ListTileControlAffinity.leading,
            contentPadding: EdgeInsets.zero,
          ),
        ],
        const SizedBox(height: 10),
        _f('Entry requirements', _entryReqCtrl,
            hint: '3 passes at A/L…', maxLines: 3),
      ]);

  Widget _campusSection() => Column(children: [
        _row2(_f('Campus name', _campusNameCtrl, hint: 'Main Campus'),
            _f('Address', _addressCtrl, hint: 'Moratuwa 10400, Sri Lanka')),
        const SizedBox(height: 10),
        _row2(
          _f('Latitude', _latCtrl,
              hint: '6.6508', keyboard: TextInputType.number),
          _f('Longitude', _lngCtrl,
              hint: '79.9729', keyboard: TextInputType.number),
        ),
        const SizedBox(height: 6),
        Text(
          'Find coordinates at openstreetmap.org',
          style:
              GoogleFonts.plusJakartaSans(fontSize: 11, color: AppColors.text3),
        ),
      ]);

  Widget _intakeSection() => Column(children: [
        _row2(
          _f('Next intake', _nextIntakeCtrl, hint: 'September 2026'),
          _dd(
              'Application status',
              _applicationStatus,
              ['Open', 'Closed', 'Coming Soon'],
              (v) => setState(() => _applicationStatus = v!)),
        ),
        const SizedBox(height: 10),
        _f('Application deadline', _deadlineCtrl, hint: '2026-08-31'),
        const SizedBox(height: 10),
        _row2(_f('Phone', _phoneCtrl, hint: '+94 11 265 0301'),
            _f('Email', _emailCtrl, hint: 'info@uom.lk')),
        const SizedBox(height: 10),
        _f('Official website', _websiteCtrl, hint: 'https://uom.lk'),
        const SizedBox(height: 10),
        _f('Degree page URL', _degreePageCtrl, hint: 'https://uom.lk/cse'),
        const SizedBox(height: 10),
        _f('Apply now URL', _applyNowCtrl, hint: 'https://ugc.ac.lk'),
      ]);

  Widget _recognitionSection() => Column(children: [
        CheckboxListTile(
          value: _ugcRecognized,
          onChanged: (v) => setState(() => _ugcRecognized = v!),
          title: Text('UGC recognized *',
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 13, color: AppColors.text1)),
          activeColor: AppColors.sky,
          controlAffinity: ListTileControlAffinity.leading,
          contentPadding: EdgeInsets.zero,
        ),
        CheckboxListTile(
          value: _ministryRecognized,
          onChanged: (v) => setState(() => _ministryRecognized = v!),
          title: Text('Ministry recognized',
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 13, color: AppColors.text1)),
          activeColor: AppColors.sky,
          controlAffinity: ListTileControlAffinity.leading,
          contentPadding: EdgeInsets.zero,
        ),
        const SizedBox(height: 10),
        _f('Accreditation', _accreditationCtrl,
            hint: 'IESL, BCS, Staffordshire University'),
        const SizedBox(height: 10),
        _f('Scholarships', _scholarshipsCtrl,
            hint: 'Merit scholarships available…', maxLines: 3),
        const SizedBox(height: 10),
        _f('Financial aid', _financialAidCtrl,
            hint: 'Bank loan facility available…', maxLines: 2),
        const SizedBox(height: 10),
        _f('Payment plans', _paymentPlansCtrl,
            hint: 'Semester-based installments…', maxLines: 2),
      ]);

  Widget _resourcesSection() => Column(children: [
        _f('Logo URL', _logoUrlCtrl,
            hint: 'https://... (publicly accessible image)'),
        const SizedBox(height: 10),
        _f('Campus image URL', _campusImageCtrl,
            hint: 'https://... (campus photo)'),
        const SizedBox(height: 10),
        _f('Virtual tour URL', _virtualTourCtrl,
            hint: 'https://youtube.com/... (campus tour)'),
        const SizedBox(height: 10),
        _f('Brochure URL (PDF)', _brochureCtrl,
            hint: 'https://... (downloadable brochure)'),
      ]);

  // ── Shared form helpers ───────────────────────────────────

  Widget _row2(Widget a, Widget b) => Row(
        children: [
          Expanded(child: a),
          const SizedBox(width: 10),
          Expanded(child: b),
        ],
      );

  Widget _f(
    String label,
    TextEditingController ctrl, {
    String hint = '',
    int maxLines = 1,
    TextInputType keyboard = TextInputType.text,
  }) =>
      Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label,
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 10,
                  fontWeight: FontWeight.w700,
                  color: AppColors.text3,
                  letterSpacing: .4)),
          const SizedBox(height: 4),
          TextField(
            controller: ctrl,
            maxLines: maxLines,
            keyboardType: keyboard,
            style: GoogleFonts.plusJakartaSans(
                fontSize: 13, color: AppColors.text1),
            decoration: InputDecoration(
              hintText: hint,
              hintStyle: GoogleFonts.plusJakartaSans(
                  fontSize: 12, color: AppColors.text3),
              filled: true,
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
            ),
          ),
        ],
      );

  Widget _dd(
    String label,
    String value,
    List<String> options,
    ValueChanged<String?> onChanged,
  ) =>
      Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label,
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 10,
                  fontWeight: FontWeight.w700,
                  color: AppColors.text3,
                  letterSpacing: .4)),
          const SizedBox(height: 4),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 12),
            decoration: BoxDecoration(
              color: AppColors.surface,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: AppColors.border),
            ),
            child: DropdownButton<String>(
              value: value,
              isExpanded: true,
              underline: const SizedBox(),
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 13, color: AppColors.text1),
              items: options
                  .map((o) => DropdownMenuItem(value: o, child: Text(o)))
                  .toList(),
              onChanged: onChanged,
            ),
          ),
        ],
      );

  Widget _errorBanner() => Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: AppColors.rosePale,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: AppColors.rose.withOpacity(.3)),
        ),
        child: Row(
          children: [
            const Icon(Icons.error_outline, color: AppColors.rose, size: 18),
            const SizedBox(width: 8),
            Expanded(
              child: Text(_error!,
                  style: GoogleFonts.plusJakartaSans(
                      fontSize: 13, color: AppColors.rose)),
            ),
          ],
        ),
      );

  @override
  void dispose() {
    for (final c in [
      _degreeNameCtrl,
      _facultyCtrl,
      _shortDescCtrl,
      _fullDescCtrl,
      _durationCtrl,
      _mediumCtrl,
      _qualificationCtrl,
      _entryReqCtrl,
      _tuitionFeeCtrl,
      _regFeeCtrl,
      _campusNameCtrl,
      _addressCtrl,
      _latCtrl,
      _lngCtrl,
      _nextIntakeCtrl,
      _deadlineCtrl,
      _phoneCtrl,
      _emailCtrl,
      _websiteCtrl,
      _degreePageCtrl,
      _applyNowCtrl,
      _accreditationCtrl,
      _scholarshipsCtrl,
      _financialAidCtrl,
      _paymentPlansCtrl,
      _logoUrlCtrl,
      _campusImageCtrl,
      _virtualTourCtrl,
      _brochureCtrl,
    ]) c.dispose();
    super.dispose();
  }
}
