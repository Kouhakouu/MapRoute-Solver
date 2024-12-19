import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data(csv_path):
    """
    Đọc dữ liệu từ file CSV.
    
    Args:
        csv_path (str): Đường dẫn đến file CSV.
    
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu.
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"Đã tải dữ liệu từ {csv_path} thành công.")
        return df
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file CSV tại {csv_path}.")
        exit(1)
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        exit(1)

def compute_statistics(df, baseline_algorithm='Dijkstra'):
    """
    Tính toán thống kê so sánh các thuật toán với thuật toán chuẩn (Dijkstra).
    
    Args:
        df (pd.DataFrame): DataFrame chứa dữ liệu.
        baseline_algorithm (str): Tên của thuật toán chuẩn để so sánh.
    
    Returns:
        pd.DataFrame: DataFrame chứa các thống kê.
    """
    # Tính toán trung bình và độ lệch chuẩn cho thời gian chạy và độ dài đường đi
    stats = df.groupby('Algorithm').agg(
        Mean_Runtime_Seconds=('Runtime_Seconds', 'mean'),
        Std_Runtime_Seconds=('Runtime_Seconds', 'std'),
        Mean_Path_Length_Meters=('Path_Length_Meters', 'mean'),
        Std_Path_Length_Meters=('Path_Length_Meters', 'std')
    ).reset_index()
    
    # Lấy thông tin của thuật toán chuẩn
    baseline = stats[stats['Algorithm'] == baseline_algorithm]
    if baseline.empty:
        print(f"Lỗi: Không tìm thấy thuật toán chuẩn '{baseline_algorithm}' trong dữ liệu.")
        exit(1)
    
    baseline_runtime = baseline['Mean_Runtime_Seconds'].values[0]
    baseline_path_length = baseline['Mean_Path_Length_Meters'].values[0]
    
    # Tính toán tỉ lệ so sánh với thuật toán chuẩn
    stats['Runtime_vs_Dijkstra'] = stats['Mean_Runtime_Seconds'] / baseline_runtime
    stats['Path_Length_vs_Dijkstra'] = stats['Mean_Path_Length_Meters'] / baseline_path_length
    
    return stats

def save_statistics(stats_df, output_path):
    """
    Lưu DataFrame thống kê vào file CSV.
    
    Args:
        stats_df (pd.DataFrame): DataFrame chứa các thống kê.
        output_path (str): Đường dẫn đến file CSV đầu ra.
    """
    try:
        stats_df.to_csv(output_path, index=False)
        print(f"Đã lưu thống kê vào {output_path}")
    except Exception as e:
        print(f"Lỗi khi lưu file thống kê: {e}")

def plot_runtime_comparison(stats_df, output_path):
    """
    Vẽ biểu đồ so sánh thời gian chạy giữa các thuật toán.
    
    Args:
        stats_df (pd.DataFrame): DataFrame chứa các thống kê.
        output_path (str): Đường dẫn đến file hình ảnh đầu ra.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Algorithm', y='Mean_Runtime_Seconds', data=stats_df, palette='viridis')
    plt.title('So Sánh Thời Gian Chạy Trung Bình Các Thuật Toán')
    plt.xlabel('Thuật Toán')
    plt.ylabel('Thời Gian Chạy Trung Bình (giây)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Đã lưu biểu đồ thời gian chạy vào {output_path}")

def plot_path_length_comparison(stats_df, output_path):
    """
    Vẽ biểu đồ so sánh độ dài đường đi trung bình giữa các thuật toán.
    
    Args:
        stats_df (pd.DataFrame): DataFrame chứa các thống kê.
        output_path (str): Đường dẫn đến file hình ảnh đầu ra.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Algorithm', y='Mean_Path_Length_Meters', data=stats_df, palette='magma')
    plt.title('So Sánh Độ Dài Đường Đi Trung Bình Các Thuật Toán')
    plt.xlabel('Thuật Toán')
    plt.ylabel('Độ Dài Đường Đi Trung Bình (mét)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Đã lưu biểu đồ độ dài đường đi vào {output_path}")

def main():
    # Đường dẫn đến file CSV kết quả từ statistics.py
    input_csv = os.path.join("statistics", "Dien Bien Ward_Ba Dinh District_Ha Noi City_Vietnam.csv")
    
    # Đường dẫn đến file CSV thống kê đầu ra
    output_stats_csv = os.path.join("statistics", "statistics_summary.csv")
    
    # Đường dẫn đến các file hình ảnh biểu đồ
    runtime_plot = os.path.join("statistics", "runtime_comparison.png")
    path_length_plot = os.path.join("statistics", "path_length_comparison.png")
    
    # Bước 1: Đọc dữ liệu
    df = load_data(input_csv)
    
    # Bước 2: Tính toán thống kê
    stats_df = compute_statistics(df, baseline_algorithm='Dijkstra')
    
    # Bước 3: Lưu thống kê vào file CSV
    save_statistics(stats_df, output_stats_csv)
    
    # Bước 4: Vẽ biểu đồ so sánh thời gian chạy
    plot_runtime_comparison(stats_df, runtime_plot)
    
    # Bước 5: Vẽ biểu đồ so sánh độ dài đường đi
    plot_path_length_comparison(stats_df, path_length_plot)
    
    print("Đã hoàn thành việc phân tích và lưu kết quả.")

if __name__ == "__main__":
    main()
