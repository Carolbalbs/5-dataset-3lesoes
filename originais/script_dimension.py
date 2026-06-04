import os
import csv
from PIL import Image
from collections import Counter

def investigate_image_sizes(base_dir, output_csv="image_dimensions_dataset_antigo.csv"):
    print(f"Investigating image sizes in: {base_dir}")
    
    image_data = []
    
    # Supported image extensions
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        image_data.append({
                            'path': file_path,
                            'directory': os.path.basename(root),
                            'filename': file,
                            'width': width,
                            'height': height,
                            'size': f"{width}x{height}"
                        })
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    if not image_data:
        print("No images found.")
        return
    
    # Save to CSV
    csv_path = os.path.join(base_dir, output_csv)
    keys = image_data[0].keys()
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
             dict_writer = csv.DictWriter(f, fieldnames=keys)
             dict_writer.writeheader()
             dict_writer.writerows(image_data)
        print(f"\nData saved to: {csv_path}")
    except Exception as e:
         print(f"Error saving CSV: {e}")
 
    total_images = len(image_data)
    sizes = [item['size'] for item in image_data]
    widths = [item['width'] for item in image_data]
    heights = [item['height'] for item in image_data]
    
    size_counts = Counter(sizes)
    
    print("\n--- Summary ---")
    print(f"Total images found: {total_images}")
    
    print("\nUnique sizes distribution:")
    for size, count in size_counts.most_common():
        print(f"  {size}: {count} images ({count/total_images*100:.2f}%)")
    
    print("\n--- Statistics per dimension ---")
    def stats(data):
        return {
            'min': min(data),
            'max': max(data),
            'avg': sum(data)/len(data)
        }
    
    w_stats = stats(widths)
    h_stats = stats(heights)
    
    print(f"Width:  Min={w_stats['min']}, Max={w_stats['max']}, Avg={w_stats['avg']:.2f}")
    print(f"Height: Min={h_stats['min']}, Max={h_stats['max']}, Avg={h_stats['avg']:.2f}")
    
    if len(size_counts) > 1:
        most_common_size = size_counts.most_common(1)[0][0]
        outliers = [item for item in image_data if item['size'] != most_common_size]
        print(f"\nImages with non-most-common sizes (Total: {len(outliers)}):")
        for item in outliers[:20]:
            print(f"  {item['path']} -> {item['size']}")
        if len(outliers) > 20:
            print(f"  ... and {len(outliers) - 20} more.")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    investigate_image_sizes(current_dir)
