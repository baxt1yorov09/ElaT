import 'package:flutter/material.dart';

/// Type scale (SPEC §7.4, §7.11). Font: Manrope (DECISIONS D4).
///
/// Manrope .ttf assets are bundled in Phase 1; until then the family name resolves to the
/// platform fallback, which keeps layout and tests stable.
abstract final class ElatTypography {
  static const String fontFamily = 'Manrope';

  static TextTheme textTheme(Color primary, Color secondary) {
    TextStyle base(double size, FontWeight weight, {double? height, Color? color}) {
      return TextStyle(
        fontFamily: fontFamily,
        fontSize: size,
        fontWeight: weight,
        height: height,
        color: color ?? primary,
      );
    }

    return TextTheme(
      // Large title 28 Bold
      displaySmall: base(28, FontWeight.w700, height: 34 / 28),
      // Section title 20 SemiBold
      titleLarge: base(20, FontWeight.w600, height: 24 / 20),
      // Card title 16 SemiBold
      titleMedium: base(16, FontWeight.w600, height: 22 / 16),
      // Body 15 Regular
      bodyLarge: base(15, FontWeight.w400, height: 22 / 15),
      bodyMedium: base(15, FontWeight.w400, height: 22 / 15),
      // Caption 13 Regular (secondary color)
      bodySmall: base(13, FontWeight.w400, height: 18 / 13, color: secondary),
      labelSmall: base(13, FontWeight.w400, height: 18 / 13, color: secondary),
      // Button 16 Bold
      labelLarge: base(16, FontWeight.w700, height: 20 / 16),
    );
  }

  /// Price label 18 Bold (SPEC §7.11).
  static const TextStyle price = TextStyle(
    fontFamily: fontFamily,
    fontSize: 18,
    fontWeight: FontWeight.w700,
  );
}
