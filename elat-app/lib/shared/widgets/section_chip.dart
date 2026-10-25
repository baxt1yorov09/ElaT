import 'package:flutter/material.dart';

import '../../core/theme/radii.dart';
import '../../core/theme/spacing.dart';

/// Section tab/chip. Selected = filled in the section color; else outlined.
class SectionChip extends StatelessWidget {
  const SectionChip({
    required this.label,
    required this.color,
    required this.selected,
    this.onTap,
    super.key,
  });

  final String label;
  final Color color;
  final bool selected;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final fg = selected ? Colors.white : color;
    final bg = selected ? color : Colors.transparent;
    return Semantics(
      button: true,
      selected: selected,
      label: label,
      child: InkWell(
        borderRadius: Radii.chipRadius,
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(
            horizontal: Spacing.s16,
            vertical: Spacing.s8,
          ),
          decoration: BoxDecoration(
            color: bg,
            borderRadius: Radii.chipRadius,
            border: Border.all(color: color),
          ),
          child: Text(
            label,
            style: Theme.of(context).textTheme.bodyMedium
                ?.copyWith(color: fg, fontWeight: FontWeight.w600),
          ),
        ),
      ),
    );
  }
}
