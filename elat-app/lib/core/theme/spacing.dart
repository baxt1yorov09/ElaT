/// 4 px spacing grid (SPEC §7.5, §7.11). No magic numbers in widgets.
abstract final class Spacing {
  static const double s4 = 4;
  static const double s8 = 8;
  static const double s12 = 12;
  static const double s16 = 16;
  static const double s24 = 24;
  static const double s32 = 32;

  /// Padding from screen edges.
  static const double screen = 16;
}

/// Component sizes (SPEC §7.11).
abstract final class Sizes {
  static const double buttonHeightPrimary = 52;
  static const double buttonHeightSecondary = 40;
  static const double minTouchTarget = 48;
  static const double bottomNavHeight = 64;
  static const double centerFabSize = 56;
  static const double iconSize = 24;
  static const double iconStroke = 1.75;
}
