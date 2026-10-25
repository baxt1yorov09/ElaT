import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../l10n/generated/app_localizations.dart';
import '../theme/colors.dart';
import '../theme/spacing.dart';

/// Bottom navigation shell with a raised center "+" button (SPEC §7.7, §7.11).
/// Height 64 px; center button 56 px, raised above the bar.
class ScaffoldWithNav extends StatelessWidget {
  const ScaffoldWithNav({required this.navigationShell, super.key});

  final StatefulNavigationShell navigationShell;

  void _go(int index) => navigationShell.goBranch(
    index,
    initialLocation: index == navigationShell.currentIndex,
  );

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final theme = Theme.of(context);

    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: _ElatBottomBar(
        currentIndex: navigationShell.currentIndex,
        onTap: _go,
        labels: [
          l10n.navHome,
          l10n.navSearch,
          l10n.navCreate,
          l10n.navChat,
          l10n.navProfile,
        ],
        borderColor: theme.dividerColor,
        backgroundColor: theme.colorScheme.surface,
        selectedColor: ElatColors.navy,
        unselectedColor: theme.textTheme.bodySmall!.color!,
      ),
    );
  }
}

class _ElatBottomBar extends StatelessWidget {
  const _ElatBottomBar({
    required this.currentIndex,
    required this.onTap,
    required this.labels,
    required this.borderColor,
    required this.backgroundColor,
    required this.selectedColor,
    required this.unselectedColor,
  });

  final int currentIndex;
  final ValueChanged<int> onTap;
  final List<String> labels;
  final Color borderColor;
  final Color backgroundColor;
  final Color selectedColor;
  final Color unselectedColor;

  static const _icons = <IconData>[
    Icons.home_outlined,
    Icons.search_outlined,
    Icons.add, // center +
    Icons.chat_bubble_outline,
    Icons.person_outline,
  ];

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      top: false,
      child: Container(
        height: Sizes.bottomNavHeight,
        decoration: BoxDecoration(
          color: backgroundColor,
          border: Border(top: BorderSide(color: borderColor)),
        ),
        child: Row(
          children: [
            for (var i = 0; i < labels.length; i++)
              Expanded(
                child: i == 2
                    ? _CenterButton(
                        label: labels[i],
                        onTap: () => onTap(i),
                        selected: currentIndex == i,
                      )
                    : _NavItem(
                        icon: _icons[i],
                        label: labels[i],
                        selected: currentIndex == i,
                        selectedColor: selectedColor,
                        unselectedColor: unselectedColor,
                        onTap: () => onTap(i),
                      ),
              ),
          ],
        ),
      ),
    );
  }
}

class _NavItem extends StatelessWidget {
  const _NavItem({
    required this.icon,
    required this.label,
    required this.selected,
    required this.selectedColor,
    required this.unselectedColor,
    required this.onTap,
  });

  final IconData icon;
  final String label;
  final bool selected;
  final Color selectedColor;
  final Color unselectedColor;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final color = selected ? selectedColor : unselectedColor;
    return InkWell(
      onTap: onTap,
      child: Semantics(
        label: label,
        selected: selected,
        button: true,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: Sizes.iconSize, color: color),
            const SizedBox(height: Spacing.s4),
            Text(
              label,
              style: TextStyle(fontSize: 11, color: color),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }
}

/// Raised Coral center button; icon is Navy (never white) per brand rule.
class _CenterButton extends StatelessWidget {
  const _CenterButton({
    required this.label,
    required this.onTap,
    required this.selected,
  });

  final String label;
  final VoidCallback onTap;
  final bool selected;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Semantics(
        label: label,
        button: true,
        child: Material(
          color: ElatColors.coral,
          shape: const CircleBorder(),
          elevation: 2,
          child: InkWell(
            customBorder: const CircleBorder(),
            onTap: onTap,
            child: const SizedBox(
              width: Sizes.centerFabSize,
              height: Sizes.centerFabSize,
              child: Icon(Icons.add, color: ElatColors.navy, size: 28),
            ),
          ),
        ),
      ),
    );
  }
}
