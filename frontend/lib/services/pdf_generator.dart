import 'dart:typed_data';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
// Note: Avoid extra font packages here; sanitize dynamic text instead
import '../models/career_report_model.dart';

// =============================================================
// EduLink PDF Generator
// Generates a complete 9-page career assessment PDF report.
// Assessment-specific: reads MCQ, writing, and report data
// from assessmentId to ensure no data mixing.
// =============================================================

class PdfGenerator {
  // EduLink brand colors
  static final _navy = PdfColor.fromInt(0xFF0F2A5C);
  static final _blue = PdfColor.fromInt(0xFF3B82F6);
  static final _mint = PdfColor.fromInt(0xFF10B981);
  static final _gold = PdfColor.fromInt(0xFFF59E0B);
  static final _rose = PdfColor.fromInt(0xFFEF4444);
  static final _grey = PdfColor.fromInt(0xFFE5E7EB);
  static final _text1 = PdfColor.fromInt(0xFF111827);
  static final _text2 = PdfColor.fromInt(0xFF6B7280);
  static final _white = PdfColors.white;

  static final _riasecColors = {
    'R': PdfColor.fromInt(0xFF3B82F6),
    'I': PdfColor.fromInt(0xFF8B5CF6),
    'A': PdfColor.fromInt(0xFFEC4899),
    'S': PdfColor.fromInt(0xFF10B981),
    'E': PdfColor.fromInt(0xFFF59E0B),
    'C': PdfColor.fromInt(0xFFEF4444),
  };

  static const _riasecLabels = {
    'R': 'Realistic',
    'I': 'Investigative',
    'A': 'Artistic',
    'S': 'Social',
    'E': 'Enterprising',
    'C': 'Conventional',
  };

  // ── Public API ───────────────────────────────────────────

  static Future<Uint8List> generate({
    required CareerReport report,
    required String assessmentId,
    required Map<String, dynamic> studentProfile,
    required String writingText,
    required Map<String, int> mcqAnswers,
  }) async {
    // Create PDF document. We sanitize dynamic strings to avoid
    // unsupported unicode characters that can render as replacement glyphs.
    final pdf = pw.Document();
    final studentId = assessmentId.contains('_')
        ? assessmentId.split('_')[0]
        : assessmentId;

    final date = _formatAssessmentDate(assessmentId);

    // Page 1 — Cover + Student Info
    pdf.addPage(
      _buildPage(
        _buildCoverPage(
          report: report,
          studentProfile: studentProfile,
          assessmentId: assessmentId,
          studentId: studentId,
          date: date,
        ),
        assessmentId: assessmentId,
        generatedDate: date,
      ),
    );

    // Page 2 — Career Recommendation
    pdf.addPage(
      _buildPage(
        _buildCareerPage(report: report),
        assessmentId: assessmentId,
        generatedDate: date,
      ),
    );

    // Page 3 — RIASEC Analysis
    pdf.addPage(
      _buildPage(
        _buildRiasecPage(report: report),
        assessmentId: assessmentId,
        generatedDate: date,
      ),
    );

    // Page 4 — Psychological Strengths
    pdf.addPage(
      _buildPage(
        _buildStrengthsPage(report: report),
        assessmentId: assessmentId,
        generatedDate: date,
      ),
    );

    // Page 5 — Communication Style + Writing Sample
    pdf.addPage(
      _buildPage(
        _buildCommunicationPage(report: report, writingText: writingText),
        assessmentId: assessmentId,
        generatedDate: date,
      ),
    );

    // Page 6 — Market Intelligence
    pdf.addPage(
      _buildPage(
        _buildMarketPage(report: report),
        assessmentId: assessmentId,
        generatedDate: date,
      ),
    );

    // Page 7 — Education + Jobs
    pdf.addPage(
      _buildPage(
        _buildEducationJobsPage(report: report),
        assessmentId: assessmentId,
        generatedDate: date,
      ),
    );

    // Page 8 — MCQ Responses
    pdf.addPage(
      _buildPage(
        _buildMCQPage(mcqAnswers: mcqAnswers),
        assessmentId: assessmentId,
        generatedDate: date,
      ),
    );

    // Page 9 — Disclaimer
    pdf.addPage(
      _buildPage(
        _buildDisclaimerPage(assessmentId: assessmentId, date: date),
        assessmentId: assessmentId,
        generatedDate: date,
      ),
    );

    return pdf.save();
  }

  // ── Page Template ────────────────────────────────────────

  static pw.Page _buildPage(
    pw.Widget content, {
    String assessmentId = '',
    String generatedDate = '',
  }) {
    return pw.Page(
      pageFormat: PdfPageFormat.a4,
      margin: pw.EdgeInsets.all(36),
      build: (context) => pw.Column(
        crossAxisAlignment: pw.CrossAxisAlignment.start,
        children: [
          pw.Expanded(child: content),
          pw.SizedBox(height: 8),
          pw.Divider(color: _grey, thickness: 0.5),
          pw.Row(
            mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
            children: [
              pw.Text(
                'Assessment ID: ${assessmentId.isNotEmpty ? assessmentId : 'Not provided'}',
                style: pw.TextStyle(fontSize: 8, color: _text2),
              ),
              pw.Row(
                children: [
                  pw.Text(
                    generatedDate.isNotEmpty ? generatedDate : '',
                    style: pw.TextStyle(fontSize: 8, color: _text2),
                  ),
                  pw.SizedBox(width: 12),
                  pw.Text(
                    'Page ${context.pageNumber} of ${context.pagesCount}',
                    style: pw.TextStyle(fontSize: 8, color: _text2),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }

  // ── Header Widget ────────────────────────────────────────

  static pw.Widget _header(String title, {String subtitle = ''}) {
    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        pw.Container(
          width: double.infinity,
          padding: pw.EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          decoration: pw.BoxDecoration(color: _navy),
          child: pw.Row(
            mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
            children: [
              pw.Text(
                'EduLink',
                style: pw.TextStyle(
                  color: _white,
                  fontSize: 14,
                  fontWeight: pw.FontWeight.bold,
                ),
              ),
              pw.Text(
                'Career Intelligence Report',
                style: pw.TextStyle(color: PdfColors.white, fontSize: 9),
              ),
            ],
          ),
        ),
        pw.SizedBox(height: 14),
        pw.Text(
          title,
          style: pw.TextStyle(
            fontSize: 16,
            fontWeight: pw.FontWeight.bold,
            color: _navy,
          ),
        ),
        if (subtitle.isNotEmpty) ...[
          pw.SizedBox(height: 3),
          pw.Text(subtitle, style: pw.TextStyle(fontSize: 9, color: _text2)),
        ],
        pw.SizedBox(height: 10),
        pw.Divider(color: _grey, thickness: 1),
        pw.SizedBox(height: 10),
      ],
    );
  }

  // ── Section Header ───────────────────────────────────────

  static pw.Widget _sectionTitle(String text) {
    return pw.Padding(
      padding: pw.EdgeInsets.only(bottom: 6, top: 10),
      child: pw.Text(
        text.toUpperCase(),
        style: pw.TextStyle(
          fontSize: 8,
          fontWeight: pw.FontWeight.bold,
          color: _text2,
          letterSpacing: 0.8,
        ),
      ),
    );
  }

  // ── Bar Chart Row ─────────────────────────────────────────

  static pw.Widget _barRow(
    String label,
    double value,
    PdfColor color, {
    double maxWidth = 180,
    double labelWidth = 130,
  }) {
    final filled = (value / 100 * maxWidth).clamp(0, maxWidth);
    final empty = maxWidth - filled;

    return pw.Padding(
      padding: pw.EdgeInsets.symmetric(vertical: 3),
      child: pw.Row(
        children: [
          pw.SizedBox(
            width: labelWidth,
            child: pw.Text(
              label,
              style: pw.TextStyle(fontSize: 9, color: _text1),
            ),
          ),
          pw.Row(
            children: [
              if (filled > 0)
                pw.Container(
                  width: filled.toDouble(),
                  height: 8,
                  decoration: pw.BoxDecoration(
                    color: color,
                    borderRadius: pw.BorderRadius.circular(2),
                  ),
                ),
              if (empty > 0)
                pw.Container(
                  width: empty.toDouble(),
                  height: 8,
                  decoration: pw.BoxDecoration(
                    color: _grey,
                    borderRadius: pw.BorderRadius.circular(2),
                  ),
                ),
            ],
          ),
          pw.SizedBox(width: 8),
          pw.Text(
            value.toStringAsFixed(1),
            style: pw.TextStyle(
              fontSize: 9,
              fontWeight: pw.FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  // ── Info Row ─────────────────────────────────────────────

  static pw.Widget _infoRow(String label, String value) {
    return pw.Padding(
      padding: pw.EdgeInsets.symmetric(vertical: 3),
      child: pw.Row(
        crossAxisAlignment: pw.CrossAxisAlignment.start,
        children: [
          pw.SizedBox(
            width: 100,
            child: pw.Text(
              label,
              style: pw.TextStyle(fontSize: 9, color: _text2),
            ),
          ),
          pw.Expanded(
            child: pw.Text(
              value,
              style: pw.TextStyle(
                fontSize: 9,
                fontWeight: pw.FontWeight.bold,
                color: _text1,
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ── Divider ───────────────────────────────────────────────

  static pw.Widget _divider() => pw.Padding(
    padding: pw.EdgeInsets.symmetric(vertical: 8),
    child: pw.Divider(color: _grey, thickness: 0.5),
  );

  // ── Page 1 — Cover + Student Info ────────────────────────

  static pw.Widget _buildCoverPage({
    required CareerReport report,
    required Map<String, dynamic> studentProfile,
    required String assessmentId,
    required String studentId,
    required String date,
  }) {
    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        // Large navy header
        pw.Container(
          width: double.infinity,
          padding: pw.EdgeInsets.all(24),
          decoration: pw.BoxDecoration(color: _navy),
          child: pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Text(
                'EduLink',
                style: pw.TextStyle(
                  color: _white,
                  fontSize: 28,
                  fontWeight: pw.FontWeight.bold,
                ),
              ),
              pw.SizedBox(height: 4),
              pw.Text(
                'AI Career Intelligence Platform',
                style: pw.TextStyle(color: PdfColors.white, fontSize: 11),
              ),
              pw.SizedBox(height: 16),
              pw.Text(
                'Career Assessment Report',
                style: pw.TextStyle(
                  color: _white,
                  fontSize: 18,
                  fontWeight: pw.FontWeight.bold,
                ),
              ),
              pw.SizedBox(height: 8),
              pw.Text(
                'Generated: $date',
                style: pw.TextStyle(color: PdfColors.white, fontSize: 9),
              ),
              pw.Text(
                'Assessment ID: $assessmentId',
                style: pw.TextStyle(color: PdfColors.white, fontSize: 9),
              ),
            ],
          ),
        ),

        pw.SizedBox(height: 20),
        _sectionTitle('Student Profile'),

        _infoRow('Name', _displayValue(report.studentName)),
        _infoRow('Student ID', _displayValue(studentId)),
        _infoRow('Age', _displayValue(studentProfile['age'])),
        _infoRow('Gender', _displayValue(_getGender(studentProfile))),
        _infoRow('School', _displayValue(studentProfile['school'])),
        _infoRow('Stream', _displayValue(studentProfile['stream'])),
        _infoRow('District', _displayValue(studentProfile['district'])),
        _infoRow('Grade', _displayValue(studentProfile['grade'])),

        _divider(),
        _sectionTitle('Assessment Summary'),

        pw.Container(
          padding: pw.EdgeInsets.all(14),
          decoration: pw.BoxDecoration(
            color: PdfColor.fromInt(0xFFF0F4FF),
            borderRadius: pw.BorderRadius.circular(6),
            border: pw.Border.all(color: _grey),
          ),
          child: pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Text(
                report.finalRole,
                style: pw.TextStyle(
                  fontSize: 18,
                  fontWeight: pw.FontWeight.bold,
                  color: _navy,
                ),
              ),
              pw.SizedBox(height: 6),
              pw.Row(
                children: [
                  pw.Text(
                    'Score: ${report.finalScore.toStringAsFixed(1)} / 100',
                    style: pw.TextStyle(
                      fontSize: 10,
                      fontWeight: pw.FontWeight.bold,
                      color: _text1,
                    ),
                  ),
                  pw.SizedBox(width: 16),
                  pw.Container(
                    padding: pw.EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 2,
                    ),
                    decoration: pw.BoxDecoration(
                      color: _confidenceColor(
                        report.confidenceLabel,
                      ).shade(0.15),
                      borderRadius: pw.BorderRadius.circular(10),
                    ),
                    child: pw.Text(
                      report.confidenceLabel,
                      style: pw.TextStyle(
                        fontSize: 9,
                        fontWeight: pw.FontWeight.bold,
                        color: _confidenceColor(report.confidenceLabel),
                      ),
                    ),
                  ),
                ],
              ),
              pw.SizedBox(height: 4),
              pw.Text(
                'Interest Code: ${report.interestCode}',
                style: pw.TextStyle(fontSize: 9, color: _text2),
              ),
            ],
          ),
        ),
      ],
    );
  }

  // ── Page 2 — Career Recommendation ───────────────────────

  static pw.Widget _buildCareerPage({required CareerReport report}) {
    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        _header('Career Recommendation'),
        _sectionTitle('Recommended Career Path'),

        pw.Container(
          width: double.infinity,
          padding: pw.EdgeInsets.all(16),
          decoration: pw.BoxDecoration(color: _navy),
          child: pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Text(
                report.finalRole,
                style: pw.TextStyle(
                  color: _white,
                  fontSize: 22,
                  fontWeight: pw.FontWeight.bold,
                ),
              ),
              pw.SizedBox(height: 4),
              pw.Text(
                'Score: ${report.finalScore.toStringAsFixed(1)} / 100  |  '
                'Confidence: ${report.confidenceLabel}',
                style: pw.TextStyle(color: PdfColors.white, fontSize: 10),
              ),
            ],
          ),
        ),

        pw.SizedBox(height: 14),
        _sectionTitle('Top Career Clusters'),

        _clusterRow('1st', report.top1Cluster, _mint),
        _clusterRow('2nd', report.top2Cluster, _blue),
        _clusterRow('3rd', report.top3Cluster, _gold),

        _divider(),
        _sectionTitle('Holland Interest Code'),

        pw.Text(
          report.interestCode,
          style: pw.TextStyle(
            fontSize: 32,
            fontWeight: pw.FontWeight.bold,
            color: _navy,
            letterSpacing: 8,
          ),
        ),
        pw.SizedBox(height: 6),
        pw.Text(
          _interestCodeDescription(report.interestCode),
          style: pw.TextStyle(fontSize: 9, color: _text2),
        ),

        _divider(),
        _sectionTitle('AI Reasoning Explanation'),

        pw.Container(
          padding: pw.EdgeInsets.all(12),
          decoration: pw.BoxDecoration(
            color: PdfColor.fromInt(0xFFF9FAFB),
            borderRadius: pw.BorderRadius.circular(6),
            border: pw.Border.all(color: _grey),
          ),
          child: pw.Text(
            _sanitize(report.finalExplanation.replaceAll(' | ', '\n')),
            style: pw.TextStyle(fontSize: 9, color: _text1, lineSpacing: 3),
          ),
        ),

        _divider(),
        _sectionTitle('Recommended Roles'),

        pw.Wrap(
          spacing: 8,
          runSpacing: 4,
          children: report.roles
              .take(6)
              .map(
                (role) => pw.Container(
                  padding: pw.EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: pw.BoxDecoration(
                    color: PdfColor.fromInt(0xFFEFF6FF),
                    borderRadius: pw.BorderRadius.circular(12),
                    border: pw.Border.all(color: _blue),
                  ),
                  child: pw.Text(
                    role,
                    style: pw.TextStyle(fontSize: 8, color: _navy),
                  ),
                ),
              )
              .toList(),
        ),
      ],
    );
  }

  // ── Page 3 — RIASEC Analysis ─────────────────────────────

  static pw.Widget _buildRiasecPage({required CareerReport report}) {
    final order = ['R', 'I', 'A', 'S', 'E', 'C'];

    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        _header(
          'RIASEC Personality Profile',
          subtitle: 'Holland Vocational Personality Theory - Six Dimensions',
        ),
        _sectionTitle('RIASEC Dimension Scores'),

        ...order.map((key) {
          final score = report.riasec[key] ?? 0.0;
          final label = _riasecLabels[key] ?? key;
          final color = _riasecColors[key] ?? _blue;
          final isTop = key == report.interestCode.isNotEmpty
              ? report.interestCode[0]
              : '';
          return _barRow(
            '$key  $label${isTop == key ? '  ★' : ''}',
            score,
            color,
          );
        }),

        _divider(),
        _sectionTitle('RIASEC Interpretation'),

        pw.Table(
          border: pw.TableBorder.all(color: _grey, width: 0.5),
          columnWidths: {
            0: const pw.FixedColumnWidth(50),
            1: const pw.FixedColumnWidth(90),
            2: const pw.FlexColumnWidth(),
          },
          children: [
            _tableHeaderRow(['Code', 'Type', 'Characteristics']),
            _tableRow([
              'R',
              'Realistic',
              'Practical, hands-on, technical problem solving',
            ]),
            _tableRow([
              'I',
              'Investigative',
              'Analytical, intellectual, data-driven inquiry',
            ]),
            _tableRow([
              'A',
              'Artistic',
              'Creative, expressive, innovative thinking',
            ]),
            _tableRow([
              'S',
              'Social',
              'Collaborative, communicative, helping others',
            ]),
            _tableRow([
              'E',
              'Enterprising',
              'Leadership, business-oriented, strategic',
            ]),
            _tableRow([
              'C',
              'Conventional',
              'Structured, organised, detail-oriented',
            ]),
          ],
        ),

        _divider(),
        _sectionTitle('Your Holland Interest Code'),

        pw.Text(
          report.interestCode.isNotEmpty
              ? 'Your three-letter code ${report.interestCode} indicates '
                    'that your strongest vocational orientations are '
                    '${_expandCode(report.interestCode)}.'
              : 'Interest code not available.',
          style: pw.TextStyle(fontSize: 9, color: _text1, lineSpacing: 3),
        ),
      ],
    );
  }

  // ── Page 4 — Psychological Strengths ─────────────────────

  static pw.Widget _buildStrengthsPage({required CareerReport report}) {
    final technical = {
      'Technical Problem Solving':
          report.topComposites['Technical_ProblemSolving'] ?? 0,
      'Tech Adaptability': report.topComposites['Tech_Adaptability'] ?? 0,
      'Process Optimisation': report.topComposites['Process_Optimization'] ?? 0,
      'Career Growth Mindset':
          report.topComposites['Career_Growth_Mindset'] ?? 0,
    };

    final analytical = {
      'Analytical Thinking': report.topComposites['Analytical_Thinking'] ?? 0,
      'Data Literacy': report.topComposites['Data_Literacy'] ?? 0,
      'Future Orientation': report.topComposites['Future_Orientation'] ?? 0,
      'Innovation Drive': report.topComposites['Innovation_Drive'] ?? 0,
    };

    final social = {
      'Leadership Capability':
          report.topComposites['Leadership_Capability'] ?? 0,
      'Creativity Index': report.topComposites['Creativity_Index'] ?? 0,
      'Social Intelligence': report.topComposites['Social_Intelligence'] ?? 0,
      'Communication Skill': report.topComposites['Communication_Skill'] ?? 0,
    };

    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        _header(
          'Psychological Strengths Profile',
          subtitle: 'Derived from 40-item psychometric assessment',
        ),

        _sectionTitle('Technical Strengths'),
        ...technical.entries.map(
          (e) => _barRow(e.key, e.value, _blue, maxWidth: 220, labelWidth: 140),
        ),

        _divider(),
        _sectionTitle('Analytical Strengths'),
        ...analytical.entries.map(
          (e) => _barRow(
            e.key,
            e.value,
            _navy.shade(0.8),
            maxWidth: 220,
            labelWidth: 140,
          ),
        ),

        _divider(),
        _sectionTitle('Social Strengths'),
        ...social.entries.map(
          (e) => _barRow(e.key, e.value, _mint, maxWidth: 220, labelWidth: 140),
        ),

        _divider(),

        pw.Container(
          padding: pw.EdgeInsets.all(10),
          decoration: pw.BoxDecoration(
            color: PdfColor.fromInt(0xFFF9FAFB),
            borderRadius: pw.BorderRadius.circular(6),
            border: pw.Border.all(color: _grey),
          ),
          child: pw.Text(
            'These composite scores are derived from the '
            'Mathematical and Psychological Processing Layer '
            'of EduLink, grounded in Holland\'s RIASEC theory, '
            'Social Cognitive Career Theory, and related '
            'psychometric frameworks.',
            style: pw.TextStyle(fontSize: 8, color: _text2, lineSpacing: 2),
          ),
        ),
      ],
    );
  }

  // ── Page 5 — Communication Style + Writing ───────────────

  static pw.Widget _buildCommunicationPage({
    required CareerReport report,
    required String writingText,
  }) {
    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        _header('Communication Style & Writing Analysis'),
        _sectionTitle('Writing Analysis Scores'),

        pw.Row(
          children: [
            pw.Text(
              'Overall Score: ',
              style: pw.TextStyle(fontSize: 10, color: _text2),
            ),
            pw.Text(
              '${report.overallWritingScore.toStringAsFixed(1)} / 100',
              style: pw.TextStyle(
                fontSize: 14,
                fontWeight: pw.FontWeight.bold,
                color: _navy,
              ),
            ),
          ],
        ),
        pw.SizedBox(height: 10),

        _barRow('Analytical Thinking', report.writingAnalytical, _blue),
        _barRow('Clarity', report.writingClarity, _blue),
        _barRow('Structure', report.writingStructure, _mint),
        _barRow('Confidence', report.writingConfidence, _gold),
        _barRow(
          'Creativity',
          report.writingCreativity,
          PdfColor.fromInt(0xFF8B5CF6),
        ),

        _divider(),
        _sectionTitle('Your Writing Sample'),

        pw.Container(
          padding: pw.EdgeInsets.all(12),
          decoration: pw.BoxDecoration(
            color: PdfColor.fromInt(0xFFF9FAFB),
            borderRadius: pw.BorderRadius.circular(6),
            border: pw.Border.all(color: _grey),
          ),
          child: pw.Text(
            writingText.isNotEmpty
                ? _sanitize(writingText)
                : 'Writing sample not available.',
            style: pw.TextStyle(
              fontSize: 9,
              color: _text1,
              lineSpacing: 3,
              fontStyle: pw.FontStyle.italic,
            ),
          ),
        ),
      ],
    );
  }

  // ── Page 6 — Market Intelligence ─────────────────────────

  static pw.Widget _buildMarketPage({required CareerReport report}) {
    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        _header('Market Intelligence'),
        _sectionTitle('Salary Estimate'),

        pw.Container(
          padding: pw.EdgeInsets.all(14),
          decoration: pw.BoxDecoration(
            color: PdfColor.fromInt(0xFFF0FDF4),
            borderRadius: pw.BorderRadius.circular(6),
            border: pw.Border.all(color: _mint),
          ),
          child: pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Text(
                'Current (Entry Level)',
                style: pw.TextStyle(
                  fontSize: 9,
                  fontWeight: pw.FontWeight.bold,
                  color: _text2,
                ),
              ),
              pw.Text(
                'LKR ${_fmtMaybe(report.salaryMin)} - ${_fmtMaybe(report.salaryMax)} per month',
                style: pw.TextStyle(
                  fontSize: 14,
                  fontWeight: pw.FontWeight.bold,
                  color: _navy,
                ),
              ),
              pw.SizedBox(height: 10),
              pw.Text(
                'Future Projection (3-5 Years)',
                style: pw.TextStyle(
                  fontSize: 9,
                  fontWeight: pw.FontWeight.bold,
                  color: _text2,
                ),
              ),
              pw.Text(
                'LKR ${_fmtMaybe(report.futureSalaryMid)} per month',
                style: pw.TextStyle(
                  fontSize: 14,
                  fontWeight: pw.FontWeight.bold,
                  color: _mint,
                ),
              ),
              pw.SizedBox(height: 6),
              pw.Text(
                'Source: ICTA Sri Lanka IT Salary Survey • Live USD/LKR rate',
                style: pw.TextStyle(fontSize: 7, color: _text2),
              ),
            ],
          ),
        ),

        _divider(),
        _sectionTitle('Market Demand'),

        pw.Container(
          padding: pw.EdgeInsets.all(12),
          decoration: pw.BoxDecoration(
            color: _demandColor(report.demandTrend).shade(0.1),
            borderRadius: pw.BorderRadius.circular(6),
            border: pw.Border.all(color: _demandColor(report.demandTrend)),
          ),
          child: pw.Row(
            children: [
              pw.Text(
                'Market Demand Trend: ',
                style: pw.TextStyle(fontSize: 10, color: _text2),
              ),
              pw.Text(
                report.demandTrend,
                style: pw.TextStyle(
                  fontSize: 12,
                  fontWeight: pw.FontWeight.bold,
                  color: _demandColor(report.demandTrend),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  // ── Page 7 — Education + Jobs ─────────────────────────────

  static pw.Widget _buildEducationJobsPage({required CareerReport report}) {
    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        _header('Education & Job Opportunities'),
        _sectionTitle('Recommended Education Programmes'),

        ...report.educationPrograms.take(5).toList().asMap().entries.map((
          entry,
        ) {
          final i = entry.key;
          final p = entry.value as Map<String, dynamic>;
          return pw.Padding(
            padding: pw.EdgeInsets.only(bottom: 8),
            child: pw.Container(
              padding: pw.EdgeInsets.all(10),
              decoration: pw.BoxDecoration(
                border: pw.Border.all(color: _grey),
                borderRadius: pw.BorderRadius.circular(6),
              ),
              child: pw.Column(
                crossAxisAlignment: pw.CrossAxisAlignment.start,
                children: [
                  pw.Text(
                    '${i + 1}. ${_sanitize(p['institute']?.toString() ?? '')}',
                    style: pw.TextStyle(
                      fontSize: 10,
                      fontWeight: pw.FontWeight.bold,
                      color: _navy,
                    ),
                  ),
                  if ((p['program_name'] ?? '').toString().isNotEmpty)
                    pw.Text(
                      _sanitize(p['program_name']?.toString() ?? ''),
                      style: pw.TextStyle(fontSize: 9, color: _blue),
                    ),
                  pw.SizedBox(height: 3),
                  pw.Text(
                    '${p['program_level'] ?? p['level'] ?? ''}  |  '
                    '${p['duration_months']} months  |  '
                    '${p['cost_level']} cost  |  '
                    '${p['delivery_mode'] ?? p['mode'] ?? ''}',
                    style: pw.TextStyle(fontSize: 8, color: _text2),
                  ),
                ],
              ),
            ),
          );
        }),

        _divider(),
        _sectionTitle('Live Job Opportunities'),

        ...report.vacancyMatches.take(5).toList().asMap().entries.map((entry) {
          final i = entry.key;
          final job = entry.value as Map<String, dynamic>;
          return pw.Padding(
            padding: pw.EdgeInsets.only(bottom: 6),
            child: pw.Row(
              crossAxisAlignment: pw.CrossAxisAlignment.start,
              children: [
                pw.Container(
                  width: 18,
                  height: 18,
                  decoration: pw.BoxDecoration(
                    color: _navy,
                    shape: pw.BoxShape.circle,
                  ),
                  child: pw.Center(
                    child: pw.Text(
                      '${i + 1}',
                      style: pw.TextStyle(color: _white, fontSize: 8),
                    ),
                  ),
                ),
                pw.SizedBox(width: 8),
                pw.Expanded(
                  child: pw.Column(
                    crossAxisAlignment: pw.CrossAxisAlignment.start,
                    children: [
                      pw.Text(
                        _sanitize(job['title']?.toString() ?? ''),
                        style: pw.TextStyle(
                          fontSize: 9,
                          fontWeight: pw.FontWeight.bold,
                          color: _text1,
                        ),
                      ),
                      pw.Text(
                        '${_sanitize(job['company']?.toString() ?? '')}  |  '
                        '${_sanitize(job['location']?.toString() ?? '')}  |  '
                        '${_sanitize(job['type']?.toString() ?? '')}',
                        style: pw.TextStyle(fontSize: 8, color: _text2),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );
        }),
      ],
    );
  }

  // ── Page 8 — MCQ Responses ───────────────────────────────

  static pw.Widget _buildMCQPage({required Map<String, int> mcqAnswers}) {
    final labels = [
      'Strongly Disagree',
      'Disagree',
      'Neutral',
      'Agree',
      'Strongly Agree',
    ];

    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        _header(
          'MCQ Assessment Responses',
          subtitle:
              '40-item Likert scale (1=Strongly Disagree to 5=Strongly Agree)',
        ),

        pw.Table(
          border: pw.TableBorder.all(color: _grey, width: 0.5),
          columnWidths: {
            0: const pw.FixedColumnWidth(35),
            1: const pw.FixedColumnWidth(18),
            2: const pw.FlexColumnWidth(),
            3: const pw.FixedColumnWidth(35),
            4: const pw.FixedColumnWidth(18),
            5: const pw.FlexColumnWidth(),
          },
          children: [
            _tableHeaderRow(['Q', 'Val', 'Response', 'Q', 'Val', 'Response']),
            ...List.generate(20, (i) {
              final q1 = i + 1;
              final q2 = i + 21;
              final v1 = mcqAnswers['Q$q1'] ?? 0;
              final v2 = mcqAnswers['Q$q2'] ?? 0;
              final l1 = v1 > 0 ? labels[v1 - 1] : 'Not provided';
              final l2 = v2 > 0 ? labels[v2 - 1] : 'Not provided';
              return _tableRow(['Q$q1', '$v1', l1, 'Q$q2', '$v2', l2]);
            }),
          ],
        ),

        _divider(),
        pw.Text(
          'Scale: 1=Strongly Disagree  2=Disagree  '
          '3=Neutral  4=Agree  5=Strongly Agree',
          style: pw.TextStyle(fontSize: 7, color: _text2),
        ),
      ],
    );
  }

  // ── Page 9 — Disclaimer ───────────────────────────────────

  static pw.Widget _buildDisclaimerPage({
    required String assessmentId,
    required String date,
  }) {
    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      mainAxisAlignment: pw.MainAxisAlignment.center,
      children: [
        _header('Important Notice & Disclaimer'),

        pw.Container(
          padding: pw.EdgeInsets.all(16),
          decoration: pw.BoxDecoration(
            border: pw.Border.all(color: _grey),
            borderRadius: pw.BorderRadius.circular(6),
          ),
          child: pw.Text(
            'This career assessment report has been generated by '
            'EduLink — an AI-based Career Intelligence Platform '
            'developed at SLTC Research University as part of a '
            'BSc Honours in Data Science research project.\n\n'
            'The recommendations in this report are based on a '
            'psychometric assessment of the student\'s responses '
            'and are intended to support — not replace — '
            'professional career guidance. Students are strongly '
            'encouraged to consult a qualified career counsellor '
            'or their institution\'s career guidance service '
            'alongside this report.\n\n'
            'Career paths are dynamic and may change based on '
            'personal growth, industry trends, and evolving '
            'interests. This report represents a snapshot of '
            'the student\'s career-readiness profile at the '
            'time of assessment.',
            style: pw.TextStyle(fontSize: 9, color: _text1, lineSpacing: 4),
          ),
        ),

        pw.SizedBox(height: 24),
        pw.Divider(color: _grey),
        pw.SizedBox(height: 12),

        _infoRow('Platform', 'EduLink AI Career Intelligence Platform'),
        _infoRow('Institution', 'SLTC Research University, Sri Lanka'),
        _infoRow('Version', 'v2.0.0'),
        _infoRow('Generated', date),
        _infoRow('Assessment ID', assessmentId),

        pw.SizedBox(height: 24),

        pw.Container(
          width: double.infinity,
          padding: pw.EdgeInsets.all(12),
          decoration: pw.BoxDecoration(color: _navy),
          child: pw.Center(
            child: pw.Text(
              'EduLink — Empowering Sri Lankan IT Careers',
              style: pw.TextStyle(
                color: _white,
                fontSize: 10,
                fontWeight: pw.FontWeight.bold,
              ),
            ),
          ),
        ),
      ],
    );
  }

  // ── Helper Widgets ────────────────────────────────────────

  static pw.Widget _clusterRow(String rank, String cluster, PdfColor color) {
    return pw.Padding(
      padding: pw.EdgeInsets.symmetric(vertical: 3),
      child: pw.Row(
        children: [
          pw.Container(
            width: 30,
            height: 16,
            decoration: pw.BoxDecoration(
              color: color,
              borderRadius: pw.BorderRadius.circular(4),
            ),
            child: pw.Center(
              child: pw.Text(
                rank,
                style: pw.TextStyle(color: _white, fontSize: 7),
              ),
            ),
          ),
          pw.SizedBox(width: 10),
          pw.Text(
            cluster.replaceAll('_', ' '),
            style: pw.TextStyle(fontSize: 10, color: _text1),
          ),
        ],
      ),
    );
  }

  static pw.TableRow _tableHeaderRow(List<String> cells) {
    return pw.TableRow(
      decoration: pw.BoxDecoration(color: _navy),
      children: cells
          .map(
            (c) => pw.Padding(
              padding: pw.EdgeInsets.all(5),
              child: pw.Text(
                c,
                style: pw.TextStyle(
                  color: _white,
                  fontSize: 8,
                  fontWeight: pw.FontWeight.bold,
                ),
              ),
            ),
          )
          .toList(),
    );
  }

  static pw.TableRow _tableRow(List<String> cells) {
    return pw.TableRow(
      children: cells
          .map(
            (c) => pw.Padding(
              padding: pw.EdgeInsets.all(5),
              child: pw.Text(
                c,
                style: pw.TextStyle(fontSize: 8, color: _text1),
              ),
            ),
          )
          .toList(),
    );
  }

  // ── Utility Functions ─────────────────────────────────────

  static String _getGender(Map<String, dynamic> profile) {
    if (profile.isEmpty) return '-';
    final keys = [
      'gender',
      'sex',
      'genderIdentity',
      'gender_identity',
      'gender_type',
    ];
    for (final k in keys) {
      final v = profile[k];
      if (v != null && v.toString().trim().isNotEmpty) {
        return v.toString();
      }
    }
    // fallback to known nested structures
    if (profile.containsKey('demographics') && profile['demographics'] is Map) {
      final demo = profile['demographics'] as Map<String, dynamic>;
      for (final k in keys) {
        final v = demo[k];
        if (v != null && v.toString().trim().isNotEmpty) return v.toString();
      }
    }
    return 'Not provided';
  }

  static String _displayValue(dynamic v) {
    if (v == null) return 'Not provided';
    final s = v.toString().trim();
    if (s.isEmpty) return 'Not provided';
    return _sanitize(s);
  }

  static String _fmtMaybe(int n) {
    if (n <= 0) return 'Not available';
    return _fmt(n);
  }

  static String _fmt(int n) {
    if (n >= 1000000) return '${(n / 1000000).toStringAsFixed(1)}M';
    if (n >= 1000) return '${(n / 1000).toStringAsFixed(0)}K';
    return n.toString();
  }

  static String _formatAssessmentDate(String assessmentId) {
    try {
      final parts = assessmentId.split('_');
      if (parts.length >= 2) {
        final datePart = parts[1];
        final year = datePart.substring(0, 4);
        final month = datePart.substring(4, 6);
        final day = datePart.substring(6, 8);
        return '$day/$month/$year';
      }
    } catch (_) {}
    return DateTime.now().toString().substring(0, 10);
  }

  static String _interestCodeDescription(String code) {
    if (code.isEmpty) return '';
    final map = {
      'R': 'Realistic',
      'I': 'Investigative',
      'A': 'Artistic',
      'S': 'Social',
      'E': 'Enterprising',
      'C': 'Conventional',
    };
    return code.split('').map((c) => map[c] ?? c).join(' — ');
  }

  static String _expandCode(String code) {
    final map = {
      'R': 'Realistic',
      'I': 'Investigative',
      'A': 'Artistic',
      'S': 'Social',
      'E': 'Enterprising',
      'C': 'Conventional',
    };
    return code.split('').map((c) => map[c] ?? c).join(', ');
  }

  static String _sanitize(String s) {
    if (s.isEmpty) return s;
    return s
        .replaceAll('\uFFFD', '')
        .replaceAll('–', '-')
        .replaceAll('—', '-')
        .replaceAll('…', '...')
        .replaceAll('“', '"')
        .replaceAll('”', '"')
        .replaceAll('’', "'")
        .replaceAll('•', '-')
        .trim();
  }

  static PdfColor _confidenceColor(String label) {
    switch (label) {
      case 'High':
        return _mint;
      case 'Medium':
        return _gold;
      default:
        return _rose;
    }
  }

  static PdfColor _demandColor(String trend) {
    switch (trend) {
      case 'Increasing':
        return _mint;
      case 'Stable':
        return _blue;
      default:
        return _rose;
    }
  }
}
