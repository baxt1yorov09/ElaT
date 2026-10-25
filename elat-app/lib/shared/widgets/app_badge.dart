import 'package:flutter/material.dart';

import '../../core/theme/colors.dart';
import '../../core/theme/radii.dart';

enum BadgeKind { free, top, verified, auction }

/// Small status badge: BEPUL (green), TOP (coral/navy), Tasdiqlangan (blue), Auksion (amber).
class AppBadge extends StatelessWidget {
  const AppBadge({required this.label, required this.kind, super.key});

  final String label;
  final BadgeKind kind;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final (bg, fg) = switch (kind) {
      // Brighter green in dark mode; Navy text keeps contrast on it.
      BadgeKind.free => isDark
          ? (ElatColors.saxovatDark, ElatColors.navy)
          : (ElatColors.saxovat, Colors.white),
      BadgeKind.top => (ElatColors.coral, ElatColors.navy), // Navy on Coral
      BadgeKind.verified => (ElatColors.savdo, Colors.white),
      BadgeKind.auction => (ElatColors.baraholka, Colors.white),
    };
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(color: bg, borderRadius: Radii.chipRadius),
      child: Text(
        label,
        style: TextStyle(color: fg, fontSize: 11, fontWeight: FontWeight.w700),
      ),
    );
  }
}
