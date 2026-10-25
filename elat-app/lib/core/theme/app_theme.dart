import 'package:flutter/material.dart';

import 'colors.dart';
import 'radii.dart';
import 'spacing.dart';
import 'typography.dart';

/// Builds the light and dark [ThemeData] from design tokens.
/// Text/icons on Coral are Navy (never white) — enforced here for buttons.
abstract final class AppTheme {
  static ThemeData light() => _build(
        brightness: Brightness.light,
        background: ElatColors.bgLight,
        card: ElatColors.cardLight,
        textPrimary: ElatColors.textPrimaryLight,
        textSecondary: ElatColors.textSecondaryLight,
        border: ElatColors.borderLight,
        sections: ElatSectionColors.light,
      );

  static ThemeData dark() => _build(
        brightness: Brightness.dark,
        background: ElatColors.bgDark,
        card: ElatColors.cardDark,
        textPrimary: ElatColors.textPrimaryDark,
        textSecondary: ElatColors.textSecondaryDark,
        border: ElatColors.borderDark,
        sections: ElatSectionColors.dark,
      );

  static ThemeData _build({
    required Brightness brightness,
    required Color background,
    required Color card,
    required Color textPrimary,
    required Color textSecondary,
    required Color border,
    required ElatSectionColors sections,
  }) {
    final colorScheme = ColorScheme(
      brightness: brightness,
      primary: ElatColors.coral,
      onPrimary: ElatColors.navy, // Navy on Coral (WCAG AA)
      secondary: ElatColors.navy,
      onSecondary: Colors.white,
      surface: card,
      onSurface: textPrimary,
      error: ElatColors.error,
      onError: Colors.white,
    );

    final textTheme = ElatTypography.textTheme(textPrimary, textSecondary);

    return ThemeData(
      useMaterial3: true,
      brightness: brightness,
      scaffoldBackgroundColor: background,
      colorScheme: colorScheme,
      textTheme: textTheme,
      fontFamily: ElatTypography.fontFamily,
      dividerColor: border,
      appBarTheme: AppBarTheme(
        backgroundColor: background,
        foregroundColor: textPrimary,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: textTheme.titleLarge,
      ),
      cardTheme: CardThemeData(
        color: card,
        elevation: 1,
        margin: EdgeInsets.zero,
        shape: const RoundedRectangleBorder(borderRadius: Radii.cardRadius),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: card,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: Spacing.s16,
          vertical: Spacing.s12,
        ),
        border: OutlineInputBorder(
          borderRadius: Radii.inputRadius,
          borderSide: BorderSide(color: border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: Radii.inputRadius,
          borderSide: BorderSide(color: border),
        ),
        focusedBorder: const OutlineInputBorder(
          borderRadius: Radii.inputRadius,
          borderSide: BorderSide(color: ElatColors.navy, width: 2),
        ),
        errorBorder: const OutlineInputBorder(
          borderRadius: Radii.inputRadius,
          borderSide: BorderSide(color: ElatColors.error),
        ),
      ),
      extensions: [sections],
    );
  }
}

extension ElatThemeX on BuildContext {
  ElatSectionColors get sections =>
      Theme.of(this).extension<ElatSectionColors>()!;
}
