import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../l10n/generated/app_localizations.dart';
import '../../../shared/widgets/empty_state.dart';
import '../../../shared/widgets/secondary_button.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(l10n.navProfile)),
      body: EmptyState(
        icon: Icons.person_outline,
        title: l10n.navProfile,
        description: l10n.emptyDescription,
        action: SecondaryButton(
          label: l10n.galleryTitle,
          icon: Icons.widgets_outlined,
          onPressed: () => context.go('/home/gallery'),
        ),
      ),
    );
  }
}
