import 'package:flutter/material.dart';

import '../../../l10n/generated/app_localizations.dart';
import '../../../shared/widgets/empty_state.dart';

class ChatScreen extends StatelessWidget {
  const ChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(l10n.navChat)),
      body: EmptyState(
        icon: Icons.chat_bubble_outline,
        title: l10n.navChat,
        description: l10n.emptyDescription,
      ),
    );
  }
}
