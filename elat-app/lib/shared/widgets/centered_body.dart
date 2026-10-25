import 'package:flutter/material.dart';

import '../../core/theme/spacing.dart';

/// Centers content and caps its width on wide screens (tablet, foldable, web)
/// so lines of text and cards stay comfortable to read.
class CenteredBody extends StatelessWidget {
  const CenteredBody({
    required this.child,
    this.maxWidth = Sizes.maxContentWidth,
    super.key,
  });

  final Widget child;
  final double maxWidth;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ConstrainedBox(
        constraints: BoxConstraints(maxWidth: maxWidth),
        child: child,
      ),
    );
  }
}
