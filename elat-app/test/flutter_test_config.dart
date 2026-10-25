import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';

/// Golden masters are generated on a developer machine but verified on CI
/// (Linux). Antialiasing and font hinting differ slightly between platforms,
/// so we allow a small per-pixel tolerance: real layout/color regressions
/// (which change a large share of pixels) still fail, while cosmetic cross-OS
/// noise passes.
const double _goldenTolerance = 0.05;

Future<void> testExecutable(FutureOr<void> Function() testMain) async {
  final current = goldenFileComparator;
  if (current is LocalFileComparator) {
    goldenFileComparator = _TolerantGoldenComparator(
      current.basedir.resolve('test.dart'),
    );
  }
  await testMain();
}

class _TolerantGoldenComparator extends LocalFileComparator {
  _TolerantGoldenComparator(super.testFile);

  @override
  Future<bool> compare(Uint8List imageBytes, Uri golden) async {
    final result = await GoldenFileComparator.compareLists(
      imageBytes,
      await getGoldenBytes(golden),
    );
    if (result.passed || result.diffPercent <= _goldenTolerance) {
      return true;
    }
    final error = await generateFailureOutput(result, golden, basedir);
    throw FlutterError(error);
  }
}
