import 'package:flutter/material.dart';

import '../../../l10n/generated/app_localizations.dart';
import '../../../shared/widgets/empty_state.dart';

class CreateScreen extends StatelessWidget {
  const CreateScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(l10n.navCreate)),
      body: EmptyState(
        icon: Icons.add_box_outlined,
        title: l10n.navCreate,
        description: l10n.emptyDescription,
      ),
    );
  }
}
