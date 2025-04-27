import java.io.IOException;
import java.nio.file.*;
import java.util.*;

public class CollectorMain {

    public static void main(String[] args) throws IOException {
        Path inputPath = Paths.get(args[0]);
        Path outputPath = Paths.get(args[1]);
        int depthLimit = -1;
        if (args.length == 3) {
            depthLimit = Integer.parseInt(args[2]);
        }

        if (!Files.exists(outputPath)) {
            Files.createDirectories(outputPath);
        }

        Map<String, Integer> nameTracker = new HashMap<>();
        copyDirectory(inputPath, inputPath, outputPath, depthLimit, nameTracker);
    }

    static void copyDirectory(Path currentPath, Path baseInput, Path baseOutput, int limit, Map<String, Integer> tracker) throws IOException {
        if (!Files.exists(currentPath)) return;

        DirectoryStream<Path> stream = Files.newDirectoryStream(currentPath);
        List<Path> entries = new ArrayList<>();
        for (Path p : stream) {
            entries.add(p);
        }

        for (int i = 0; i < entries.size(); i++) {
            Path entry = entries.get(i);
            Path relativePath = baseInput.relativize(entry);
            Path parentDir = relativePath.getParent();

            if (Files.isRegularFile(entry)) {
                String fileName = entry.getFileName().toString();
                if (!fileName.isEmpty() && fileName.charAt(0) == '.') continue;

                List<String> segments = splitIntoParts(parentDir);

                if (limit != -1) {
                    while (segments.size() > limit - 1) {
                        segments.remove(0);
                    }
                }

                Path destination = baseOutput;
                for (int j = 0; j < segments.size(); j++) {
                    destination = destination.resolve(segments.get(j));
                }

                if (!Files.exists(destination)) {
                    Files.createDirectories(destination);
                }

                Path finalDest = destination.resolve(fileName);
                String finalName = fileName;

                if (tracker.containsKey(finalDest.toString())) {
                    int count = tracker.get(finalDest.toString()) + 1;
                    finalName = generateNewName(fileName, count);
                    tracker.put(destination.resolve(finalName).toString(), count);
                } else {
                    tracker.put(finalDest.toString(), 0);
                }

                Files.copy(entry, destination.resolve(finalName), StandardCopyOption.REPLACE_EXISTING);

            } else if (Files.isDirectory(entry)) {
                copyDirectory(entry, baseInput, baseOutput, limit, tracker);
            }
        }
    }

    static List<String> splitIntoParts(Path path) {
        List<String> result = new ArrayList<>();
        if (path != null) {
            for (Path element : path) {
                result.add(element.toString());
            }
        }
        return result;
    }

    static String generateNewName(String originalName, int counter) {
        int lastDot = originalName.lastIndexOf('.');
        if (lastDot == -1) {
            return originalName + "_" + counter;
        } else {
            return originalName.substring(0, lastDot) + "_" + counter + originalName.substring(lastDot);
        }
    }
}
