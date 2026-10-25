import 'package:flutter/widgets.dart';

/// Corner radii (SPEC §7.5, §7.11).
abstract final class Radii {
  static const double card = 16;
  static const double button = 14;
  static const double input = 12;
  static const double chip = 999;

  static const BorderRadius cardRadius = BorderRadius.all(
    Radius.circular(card),
  );
  static const BorderRadius buttonRadius = BorderRadius.all(
    Radius.circular(button),
  );
  static const BorderRadius inputRadius = BorderRadius.all(
    Radius.circular(input),
  );
  static const BorderRadius chipRadius = BorderRadius.all(
    Radius.circular(chip),
  );
}
