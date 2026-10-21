import 'package:flutter/material.dart';

import '../../core/theme/colors.dart';
import '../../core/theme/radii.dart';
import '../../core/theme/spacing.dart';
import '../../core/theme/typography.dart';
import 'app_badge.dart';

/// Minimal view model for a card. Replaced by domain entities in Phase 1.
class ListingCardData {
  const ListingCardData({
    required this.title,
    required this.location,
    required this.timeAgo,
    this.priceLabel,
    this.isFree = false,
    this.isTop = false,
    this.imageUrl,
  });

  final String title;
  final String location;
  final String timeAgo;
  final String? priceLabel;
  final bool isFree;
  final bool isTop;
  final String? imageUrl;
}

enum ListingCardLayout { grid, list }

/// Listing card in grid (4:3 image on top) or list (image left) layout (SPEC §7.6, §7.11).
class ListingCard extends StatelessWidget {
  const ListingCard({
    required this.data,
    this.layout = ListingCardLayout.grid,
    this.onTap,
    this.onFavorite,
    this.isFavorite = false,
    this.freeLabel = 'BEPUL',
    this.topLabel = 'TOP',
    super.key,
  });

  final ListingCardData data;
  final ListingCardLayout layout;
  final VoidCallback? onTap;
  final VoidCallback? onFavorite;
  final bool isFavorite;
  final String freeLabel;
  final String topLabel;

  @override
  Widget build(BuildContext context) {
    final card = Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: layout == ListingCardLayout.grid ? _grid(context) : _list(context),
      ),
    );
    return card;
  }

  Widget _image(BuildContext context, {double? width, double? height}) {
    return Stack(
      children: [
        Container(
          width: width,
          height: height,
          color: Theme.of(context).dividerColor,
          child: const Icon(Icons.image_outlined, color: Colors.white54),
        ),
        if (data.isFree || data.isTop)
          Positioned(
            top: Spacing.s8,
            left: Spacing.s8,
            child: data.isFree
                ? AppBadge(label: freeLabel, kind: BadgeKind.free)
                : AppBadge(label: topLabel, kind: BadgeKind.top),
          ),
        Positioned(
          top: Spacing.s4,
          right: Spacing.s4,
          child: IconButton(
            onPressed: onFavorite,
            icon: Icon(
              isFavorite ? Icons.favorite : Icons.favorite_border,
              color: isFavorite ? ElatColors.coral : Colors.white,
            ),
            tooltip: 'Sevimli',
          ),
        ),
      ],
    );
  }

  Widget _priceOrFree(BuildContext context) {
    if (data.isFree) {
      return Text(
        freeLabel,
        style: ElatTypography.price.copyWith(color: ElatColors.saxovatText),
      );
    }
    return Text(data.priceLabel ?? '', style: ElatTypography.price);
  }

  Widget _grid(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        AspectRatio(aspectRatio: 4 / 3, child: _image(context)),
        Padding(
          padding: const EdgeInsets.all(Spacing.s8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                data.title,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: theme.textTheme.titleMedium,
              ),
              const SizedBox(height: Spacing.s4),
              _priceOrFree(context),
              const SizedBox(height: Spacing.s4),
              Text('${data.location} · ${data.timeAgo}', style: theme.textTheme.bodySmall),
            ],
          ),
        ),
      ],
    );
  }

  Widget _list(BuildContext context) {
    final theme = Theme.of(context);
    return SizedBox(
      height: 104,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ClipRRect(
            borderRadius: const BorderRadius.only(
              topLeft: Radius.circular(Radii.card),
              bottomLeft: Radius.circular(Radii.card),
            ),
            child: _image(context, width: 104, height: 104),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(Spacing.s8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    data.title,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: theme.textTheme.titleMedium,
                  ),
                  const Spacer(),
                  _priceOrFree(context),
                  const SizedBox(height: Spacing.s4),
                  Text('${data.location} · ${data.timeAgo}', style: theme.textTheme.bodySmall),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
