import 'package:flutter/animation.dart';

/// Motion tokens (SPEC §17.1). Durations in ms; curves ease-out in, ease-in out.
/// Respect MediaQuery.disableAnimations: see [Motion.scaled].
abstract final class Motion {
  /// Short: tap, toggle (100–150 ms).
  static const Duration short = Duration(milliseconds: 120);

  /// Medium: card, dialog (200–250 ms).
  static const Duration medium = Duration(milliseconds: 220);

  /// Large: screen transition, bottom sheet (300–350 ms).
  static const Duration large = Duration(milliseconds: 320);

  /// Enter curve: fast start, slows down.
  static const Curve easeOut = Curves.easeOutCubic;

  /// Exit curve.
  static const Curve easeIn = Curves.easeInCubic;

  /// When reduce-motion is on, collapse to a 100 ms fade (no translation/parallax).
  static Duration scaled(Duration base, {required bool disableAnimations}) {
    return disableAnimations ? const Duration(milliseconds: 100) : base;
  }
}
