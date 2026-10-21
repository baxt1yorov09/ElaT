import 'package:flutter/material.dart';

import '../../core/theme/colors.dart';
import '../../core/theme/radii.dart';

enum SnackKind { info, success, error }

/// Shows a themed snackbar (SPEC §7.6, §17.3). Error uses a red accent.
void showAppSnackbar(
  BuildContext context, {
  required String message,
  SnackKind kind = SnackKind.info,
}) {
  final accent = switch (kind) {
    SnackKind.info => ElatColors.navy,
    SnackKind.success => ElatColors.success,
    SnackKind.error => ElatColors.error,
  };
  ScaffoldMessenger.of(context)
    ..hideCurrentSnackBar()
    ..showSnackBar(
      SnackBar(
        behavior: SnackBarBehavior.floating,
        backgroundColor: Theme.of(context).colorScheme.surface,
        duration: const Duration(seconds: 3),
        shape: const RoundedRectangleBorder(borderRadius: Radii.inputRadius),
        content: Row(
          children: [
            Container(width: 4, height: 28, color: accent),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                message,
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ),
          ],
        ),
      ),
    );
}
