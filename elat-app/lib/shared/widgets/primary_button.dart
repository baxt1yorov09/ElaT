import 'package:flutter/material.dart';

import '../../core/theme/colors.dart';
import '../../core/theme/radii.dart';
import '../../core/theme/spacing.dart';

/// Primary call-to-action: Coral fill, Navy label/spinner (never white), height 52.
class PrimaryButton extends StatelessWidget {
  const PrimaryButton({
    required this.label,
    required this.onPressed,
    this.loading = false,
    this.icon,
    super.key,
  });

  final String label;
  final VoidCallback? onPressed;
  final bool loading;
  final IconData? icon;

  @override
  Widget build(BuildContext context) {
    final enabled = onPressed != null && !loading;
    return SizedBox(
      height: Sizes.buttonHeightPrimary,
      child: FilledButton(
        onPressed: enabled ? onPressed : null,
        style: FilledButton.styleFrom(
          backgroundColor: ElatColors.coral,
          foregroundColor: ElatColors.navy,
          disabledBackgroundColor: ElatColors.coral.withValues(alpha: 0.5),
          disabledForegroundColor: ElatColors.navy.withValues(alpha: 0.6),
          shape: const RoundedRectangleBorder(borderRadius: Radii.buttonRadius),
          textStyle: Theme.of(context).textTheme.labelLarge,
        ),
        child: loading
            ? const SizedBox(
                width: 22,
                height: 22,
                child: CircularProgressIndicator(
                  strokeWidth: 2.5,
                  color: ElatColors.navy,
                ),
              )
            : Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  if (icon != null) ...[
                    Icon(icon, size: Sizes.iconSize, color: ElatColors.navy),
                    const SizedBox(width: Spacing.s8),
                  ],
                  Text(label),
                ],
              ),
      ),
    );
  }
}
