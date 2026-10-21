import 'package:flutter/material.dart';

import '../../core/theme/colors.dart';
import '../../core/theme/radii.dart';
import '../../core/theme/spacing.dart';

/// Secondary action: outlined, Navy content, height 40.
class SecondaryButton extends StatelessWidget {
  const SecondaryButton({
    required this.label,
    required this.onPressed,
    this.icon,
    super.key,
  });

  final String label;
  final VoidCallback? onPressed;
  final IconData? icon;

  @override
  Widget build(BuildContext context) {
    final color = Theme.of(context).colorScheme.onSurface;
    return SizedBox(
      height: Sizes.buttonHeightSecondary,
      child: OutlinedButton(
        onPressed: onPressed,
        style: OutlinedButton.styleFrom(
          foregroundColor: color,
          side: BorderSide(color: Theme.of(context).dividerColor),
          shape: const RoundedRectangleBorder(borderRadius: Radii.buttonRadius),
          textStyle: Theme.of(context).textTheme.labelLarge?.copyWith(fontSize: 15),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (icon != null) ...[
              Icon(icon, size: 20, color: ElatColors.navy),
              const SizedBox(width: Spacing.s8),
            ],
            Text(label),
          ],
        ),
      ),
    );
  }
}
