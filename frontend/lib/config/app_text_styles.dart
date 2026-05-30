import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

class AppTextStyles {
  static TextStyle heading1 = GoogleFonts.playfairDisplay(
    fontSize: 28,
    fontWeight: FontWeight.w700,
    color: Colors.white,
  );
  static TextStyle heading2 = GoogleFonts.playfairDisplay(
    fontSize: 22,
    fontWeight: FontWeight.w600,
    color: AppColors.navy,
  );
  static TextStyle body = GoogleFonts.plusJakartaSans(
    fontSize: 14,
    color: AppColors.text1,
  );
  static TextStyle bodySmall = GoogleFonts.plusJakartaSans(
    fontSize: 12,
    color: AppColors.text2,
  );
  static TextStyle caption = GoogleFonts.plusJakartaSans(
    fontSize: 11,
    color: AppColors.text3,
  );
  static TextStyle button = GoogleFonts.plusJakartaSans(
    fontSize: 15,
    fontWeight: FontWeight.w600,
    color: Colors.white,
  );
  static TextStyle label = GoogleFonts.plusJakartaSans(
    fontSize: 11,
    fontWeight: FontWeight.w600,
    color: AppColors.text2,
    letterSpacing: 0.5,
  );
}
