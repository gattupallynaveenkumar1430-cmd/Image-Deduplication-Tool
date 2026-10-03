import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox


# =========================================================
# IMAGE EXTENSIONS
# =========================================================

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp"
)


# =========================================================
# GLOBAL VARIABLES
# =========================================================

folder = ""
images = []
duplicate_groups = {}


# =========================================================
# SHA-256 HASHING
# =========================================================

def calculate_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


# =========================================================
# MERGE SORT
# =========================================================

def merge_sort(arr):

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i][0] <= right[j][0]:

            result.append(left[i])
            i += 1

        else:

            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# =========================================================
# LINEAR SEARCH
# =========================================================

def linear_search(arr, target):

    comparisons = 0

    for i in range(len(arr)):

        comparisons += 1

        if arr[i][0].lower() == target.lower():

            return i, comparisons

    return -1, comparisons


# =========================================================
# BINARY SEARCH
# =========================================================

def binary_search(arr, target):

    low = 0
    high = len(arr) - 1

    comparisons = 0

    target = target.lower()

    while low <= high:

        mid = (low + high) // 2

        comparisons += 1

        current = arr[mid][0].lower()

        if current == target:

            return mid, comparisons

        elif current < target:

            low = mid + 1

        else:

            high = mid - 1

    return -1, comparisons


# =========================================================
# FORMAT STORAGE
# =========================================================

def format_size(size):

    if size < 1024:

        return f"{size} B"

    elif size < 1024 * 1024:

        return f"{size / 1024:.2f} KB"

    elif size < 1024 * 1024 * 1024:

        return f"{size / (1024 * 1024):.2f} MB"

    else:

        return f"{size / (1024 * 1024 * 1024):.2f} GB"


# =========================================================
# SELECT FOLDER
# =========================================================

def select_folder():

    global folder

    selected_folder = filedialog.askdirectory()

    if selected_folder:

        folder = selected_folder

        folder_label.config(
            text=f"Selected Folder: {folder}"
        )

        status_label.config(
            text="Folder selected. Click SCAN IMAGES."
        )


# =========================================================
# SCAN IMAGES
# =========================================================

def scan_images():

    global images
    global duplicate_groups

    images = []
    duplicate_groups = {}

    if folder == "":

        messagebox.showwarning(
            "Warning",
            "Please select a folder first!"
        )

        return


    if not os.path.exists(folder):

        messagebox.showerror(
            "Error",
            "Folder not found!"
        )

        return


    result_text.delete(
        "1.0",
        tk.END
    )


    status_label.config(
        text="Scanning images..."
    )

    root.update()


    # =====================================================
    # READ IMAGE FILES
    # =====================================================

    for file in os.listdir(folder):

        if file.lower().endswith(IMAGE_EXTENSIONS):

            path = os.path.join(
                folder,
                file
            )

            try:

                size = os.path.getsize(path)

                file_hash = calculate_hash(path)

                images.append(
                    [
                        file,
                        size,
                        file_hash,
                        path
                    ]
                )

            except Exception as error:

                print(
                    f"Could not process {file}: {error}"
                )


    # =====================================================
    # MERGE SORT
    # =====================================================

    images = merge_sort(images)


    # =====================================================
    # HASH TABLE
    # =====================================================

    hash_table = {}


    for image in images:

        file_name = image[0]

        file_hash = image[2]

        if file_hash not in hash_table:

            hash_table[file_hash] = []

        hash_table[file_hash].append(
            file_name
        )


    # =====================================================
    # DUPLICATE GROUPS
    # =====================================================

    for file_hash, files in hash_table.items():

        if len(files) > 1:

            duplicate_groups[file_hash] = files


    # =====================================================
    # STATISTICS
    # =====================================================

    total_images = len(images)

    duplicate_group_count = len(
        duplicate_groups
    )

    duplicate_file_count = 0

    storage_savings = 0


    for file_hash, files in duplicate_groups.items():

        removable_files = len(files) - 1

        duplicate_file_count += removable_files


        # All identical files have same size.
        # Save the size of removable copies.

        for image in images:

            if image[0] in files:

                storage_savings += (
                    image[1] * removable_files
                )

                break


    # =====================================================
    # DISPLAY MAIN RESULT
    # =====================================================

    result_text.insert(
        tk.END,
        "IMAGE FILE DEDUPLICATION REPORT\n"
    )

    result_text.insert(
        tk.END,
        "========================================\n\n"
    )


    result_text.insert(
        tk.END,
        f"Selected Folder:\n{folder}\n\n"
    )


    result_text.insert(
        tk.END,
        "STATISTICS\n"
    )

    result_text.insert(
        tk.END,
        "----------------------------------------\n"
    )


    result_text.insert(
        tk.END,
        f"Total Images        : {total_images}\n"
    )

    result_text.insert(
        tk.END,
        f"Duplicate Groups    : "
        f"{duplicate_group_count}\n"
    )

    result_text.insert(
        tk.END,
        f"Duplicate Files     : "
        f"{duplicate_file_count}\n"
    )

    result_text.insert(
        tk.END,
        f"Potential Savings   : "
        f"{format_size(storage_savings)}\n\n"
    )


    # =====================================================
    # DUPLICATE GROUP DISPLAY
    # =====================================================

    result_text.insert(
        tk.END,
        "DUPLICATE GROUPS\n"
    )

    result_text.insert(
        tk.END,
        "========================================\n"
    )


    if duplicate_group_count == 0:

        result_text.insert(
            tk.END,
            "\nNo duplicate images found.\n"
        )

    else:

        group_number = 1


        for file_hash, files in duplicate_groups.items():

            result_text.insert(
                tk.END,
                f"\nGroup {group_number}\n"
            )

            result_text.insert(
                tk.END,
                "----------------------------------------\n"
            )


            for file in files:

                result_text.insert(
                    tk.END,
                    f"  • {file}\n"
                )


            group_number += 1


    # =====================================================
    # FINISH
    # =====================================================

    status_label.config(
        text="Scan completed successfully."
    )


# =========================================================
# SEARCH IMAGE
# =========================================================

def search_image():

    if not images:

        messagebox.showwarning(
            "Warning",
            "Please scan images first!"
        )

        return


    target = search_entry.get().strip()


    if target == "":

        messagebox.showwarning(
            "Warning",
            "Please enter an image name!"
        )

        return


    # =====================================================
    # LINEAR SEARCH
    # =====================================================

    linear_index, linear_comparisons = linear_search(
        images,
        target
    )


    # =====================================================
    # BINARY SEARCH
    # =====================================================

    binary_index, binary_comparisons = binary_search(
        images,
        target
    )


    # =====================================================
    # SEARCH RESULT
    # =====================================================

    result_text.insert(
        tk.END,
        "\n\nSEARCH COMPARISON\n"
    )

    result_text.insert(
        tk.END,
        "========================================\n"
    )


    if binary_index != -1:

        result_text.insert(
            tk.END,
            f"Image Found       : {images[binary_index][0]}\n"
        )

        result_text.insert(
            tk.END,
            f"File Size         : "
            f"{format_size(images[binary_index][1])}\n"
        )

        result_text.insert(
            tk.END,
            f"SHA-256 Hash      : "
            f"{images[binary_index][2]}\n\n"
        )

    else:

        result_text.insert(
            tk.END,
            f"Image Not Found   : {target}\n\n"
        )


    # =====================================================
    # SEARCH COMPARISON
    # =====================================================

    result_text.insert(
        tk.END,
        "ALGORITHM COMPARISON\n"
    )

    result_text.insert(
        tk.END,
        "----------------------------------------\n"
    )


    result_text.insert(
        tk.END,
        f"Linear Search Comparisons : "
        f"{linear_comparisons}\n"
    )

    result_text.insert(
        tk.END,
        f"Binary Search Comparisons : "
        f"{binary_comparisons}\n\n"
    )


    result_text.insert(
        tk.END,
        "Time Complexity\n"
    )

    result_text.insert(
        tk.END,
        "Linear Search : O(n)\n"
    )

    result_text.insert(
        tk.END,
        "Binary Search : O(log n)\n"
    )


# =========================================================
# CLEAR RESULTS
# =========================================================

def clear_results():

    result_text.delete(
        "1.0",
        tk.END
    )

    search_entry.delete(
        0,
        tk.END
    )

    duplicate_label.config(
        text="Duplicate Groups: 0 | Duplicate Files: 0 | Potential Savings: 0 B"
    )

    status_label.config(
        text="Ready."


    )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Image File Deduplication Tool"
)

root.geometry(
    "1000x750"
)

root.resizable(
    True,
    True
)


# =========================================================
# TITLE
# =========================================================

title_label = tk.Label(
    root,
    text="IMAGE FILE DEDUPLICATION TOOL",
    font=("Arial", 22, "bold")
)

title_label.pack(
    pady=(20, 5)
)


# =========================================================
# SUBTITLE
# =========================================================

subtitle_label = tk.Label(
    root,
    text="Hashing • Sorting • Searching • Duplicate Detection",
    font=("Arial", 11)
)

subtitle_label.pack(
    pady=(0, 15)
)


# =========================================================
# SELECT FOLDER BUTTON
# =========================================================

select_button = tk.Button(
    root,
    text="SELECT FOLDER",
    command=select_folder,
    width=20,
    height=2
)

select_button.pack(
    pady=5
)


# =========================================================
# FOLDER LABEL
# =========================================================

folder_label = tk.Label(
    root,
    text="No folder selected",
    wraplength=900,
    font=("Arial", 10)
)

folder_label.pack(
    pady=5
)


# =========================================================
# SCAN BUTTON
# =========================================================

scan_button = tk.Button(
    root,
    text="SCAN IMAGES",
    command=scan_images,
    width=20,
    height=2
)

scan_button.pack(
    pady=8
)


# =========================================================
# STATISTICS LABEL
# =========================================================

duplicate_label = tk.Label(
    root,
    text=(
        "Duplicate Groups: 0   |   "
        "Duplicate Files: 0   |   "
        "Potential Savings: 0 B"
    ),
    font=("Arial", 11, "bold")
)

duplicate_label.pack(
    pady=8
)


# =========================================================
# SEARCH FRAME
# =========================================================

search_frame = tk.Frame(
    root
)

search_frame.pack(
    pady=10
)


search_label = tk.Label(
    search_frame,
    text="Image Name:"
)

search_label.pack(
    side=tk.LEFT,
    padx=5
)


search_entry = tk.Entry(
    search_frame,
    width=35
)

search_entry.pack(
    side=tk.LEFT,
    padx=5
)


search_button = tk.Button(
    search_frame,
    text="SEARCH",
    command=search_image,
    width=12
)

search_button.pack(
    side=tk.LEFT,
    padx=5
)


# =========================================================
# CLEAR BUTTON
# =========================================================

clear_button = tk.Button(
    root,
    text="CLEAR RESULTS",
    command=clear_results,
    width=20
)

clear_button.pack(
    pady=5
)


# =========================================================
# STATUS
# =========================================================

status_label = tk.Label(
    root,
    text="Ready.",
    font=("Arial", 10)
)

status_label.pack(
    pady=5
)


# =========================================================
# RESULT BOX
# =========================================================

result_text = tk.Text(
    root,
    width=115,
    height=28,
    font=("Consolas", 10)
)

result_text.pack(
    padx=20,
    pady=10,
    fill=tk.BOTH,
    expand=True
)


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()