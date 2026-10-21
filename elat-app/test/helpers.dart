import 'package:elat/core/theme/app_theme.dart';
import 'package:flutter/material.dart';

/// Wraps [child] in a themed MaterialApp for widget tests (no l10n needed).
Widget wrap(Widget child, {Brightness brightness = Brightness.light}) {
  return MaterialApp(
    theme: brightness == Brightness.light ? AppTheme.light() : AppTheme.dark(),
    home: Scaffold(body: Center(child: child)),
  );
}
