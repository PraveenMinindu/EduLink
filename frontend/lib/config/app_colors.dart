import 'package:flutter/material.dart';

class AppColors {
  // Primary
  static const Color navy = Color(0xFF0F2A5C);
  static const Color navyLight = Color(0xFF1F3A7A);
  static const Color blue = Color(0xFF2563EB);
  static const Color bluePale = Color(0xFFEFF6FF);
  static const Color blueMid = Color(0xFFBFDBFE);

  // Status
  static const Color mint = Color(0xFF10B981);
  static const Color mintPale = Color(0xFFECFDF5);
  static const Color gold = Color(0xFFF59E0B);
  static const Color goldPale = Color(0xFFFFFBEB);
  static const Color rose = Color(0xFFF43F5E);
  static const Color rosePale = Color(0xFFFFF1F2);
  static const Color violet = Color(0xFF8B5CF6);
  static const Color violetPale = Color(0xFFF5F3FF);

  // Neutral
  static const Color surface = Color(0xFFF0F4FF);
  static const Color card = Color(0xFFFFFFFF);
  static const Color border = Color(0xFFDDE5F5);
  static const Color text1 = Color(0xFF09142B);
  static const Color text2 = Color(0xFF4A5878);
  static const Color text3 = Color(0xFF8C9AB5);

  // ── RIASEC personality colours ───────────────────────────
  // Used in radar chart, legend, interpretation text
  static const Color riasecR = Color(0xFF0891B2); // Realistic      — cyan
  static const Color riasecRPale = Color(0xFFECFEFF);
  static const Color riasecI = Color(0xFF2563EB); // Investigative  — blue
  static const Color riasecIPale = Color(0xFFEFF6FF);
  static const Color riasecA = Color(0xFFD97706); // Artistic       — amber
  static const Color riasecAPale = Color(0xFFFFFBEB);
  static const Color riasecS = Color(0xFF6B7280); // Social         — grey
  static const Color riasecSPale = Color(0xFFF9FAFB);
  static const Color riasecE = Color(0xFFDC2626); // Enterprising   — red
  static const Color riasecEPale = Color(0xFFFEF2F2);
  static const Color riasecC = Color(0xFF7C3AED); // Conventional   — purple
  static const Color riasecCPale = Color(0xFFF5F3FF);

  // ── Composite bar tab colours ────────────────────────────
  // One colour per tab — all bars in that tab share same colour
  static const Color compTechnical = Color(0xFF0891B2); // cyan/teal
  static const Color compAnalytical = Color(0xFF2563EB); // blue
  static const Color compSocial = Color(0xFF8B5CF6); // violet
}
