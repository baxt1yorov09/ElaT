import 'package:flutter/material.dart';

/// Brand and semantic colors (SPEC §7.3, §7.11).
///
/// Rule: text and icons on Coral are Navy (#1F2A44), never white (WCAG AA).
/// Section colors are only used within their own section.
abstract final class ElatColors {
  // Brand
  static const navy = Color(0xFF1F2A44);
  static const coral = Color(0xFFFF6B4A);

  // Section colors
  static const saxovat = Color(0xFF2E9E5B);
  static const savdo = Color(0xFF2563EB);
  static const baraholka = Color(0xFFD98E04);
  static const swap = Color(0xFF7A4FD1);

  // Darker section tints for small text on light backgrounds (§7.11)
  static const saxovatText = Color(0xFF1B6B3F);
  static const baraholkaText = Color(0xFF7A4F00);

  // Semantic
  static const success = Color(0xFF1E8E4E);
  static const warning = Color(0xFFF5B301);
  static const error = Color(0xFFD93636);

  // Light theme neutrals
  static const bgLight = Color(0xFFFAF8F5);
  static const cardLight = Color(0xFFFFFFFF);
  static const textPrimaryLight = Color(0xFF1B1F27);
  static const textSecondaryLight = Color(0xFF5F6877);
  static const borderLight = Color(0xFFE6E2DC);

  // Dark theme neutrals (§7.3)
  static const bgDark = Color(0xFF14171F);
  static const cardDark = Color(0xFF1D212B);
  static const textPrimaryDark = Color(0xFFF2F4F8);
  static const textSecondaryDark = Color(0xFF9AA4B2);
  static const borderDark = Color(0xFF2B313D);
  static const saxovatDark = Color(0xFF4CC184);
}

/// Section accent colors exposed through the theme so widgets never hardcode them.
@immutable
class ElatSectionColors extends ThemeExtension<ElatSectionColors> {
  const ElatSectionColors({
    required this.saxovat,
    required this.savdo,
    required this.baraholka,
    required this.swap,
  });

  final Color saxovat;
  final Color savdo;
  final Color baraholka;
  final Color swap;

  static const light = ElatSectionColors(
    saxovat: ElatColors.saxovat,
    savdo: ElatColors.savdo,
    baraholka: ElatColors.baraholka,
    swap: ElatColors.swap,
  );

  static const dark = ElatSectionColors(
    saxovat: ElatColors.saxovatDark,
    savdo: ElatColors.savdo,
    baraholka: ElatColors.baraholka,
    swap: ElatColors.swap,
  );

  @override
  ElatSectionColors copyWith({
    Color? saxovat,
    Color? savdo,
    Color? baraholka,
    Color? swap,
  }) {
    return ElatSectionColors(
      saxovat: saxovat ?? this.saxovat,
      savdo: savdo ?? this.savdo,
      baraholka: baraholka ?? this.baraholka,
      swap: swap ?? this.swap,
    );
  }

  @override
  ElatSectionColors lerp(ElatSectionColors? other, double t) {
    if (other == null) return this;
    return ElatSectionColors(
      saxovat: Color.lerp(saxovat, other.saxovat, t)!,
      savdo: Color.lerp(savdo, other.savdo, t)!,
      baraholka: Color.lerp(baraholka, other.baraholka, t)!,
      swap: Color.lerp(swap, other.swap, t)!,
    );
  }
}
