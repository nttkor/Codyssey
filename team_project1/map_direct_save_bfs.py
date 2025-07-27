# map_direct_save.py

import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np # 사용자 요청으로 제거
# import itertools # 사용자 요청으로 제거
# import heapq # A* 알고리즘의 우선순위 큐를 위해 사용자 요청으로 제거

# --- 1단계: 데이터 분석 및 전처리 함수 ---

def load_and_process_data(area_category_path, area_map_path, area_struct_path):
    '''
    세 개의 CSV 파일을 로드하고 병합하여 지도 시각화에 필요한
    최종 데이터프레임을 반환합니다.

    Args:
        area_category_path (str): area_category.csv 파일 경로
        area_map_path (str): area_map.csv 파일 경로
        area_struct_path (str): area_struct.csv 파일 경로

    Returns:
        pandas.DataFrame: 병합 및 전처리된 데이터프레임
    '''
    try:
        area_category_df = pd.read_csv(area_category_path)
        area_map_df = pd.read_csv(area_map_path)
        area_struct_df = pd.read_csv(area_struct_path)
    except FileNotFoundError as e:
        print(f'Error loading file: {e}. Please ensure all CSV files are in the same directory.')
        exit()

    # 열 이름의 공백 제거 (사용자 수정 반영)
    area_category_df.columns = area_category_df.columns.str.strip()
    area_map_df.columns = area_map_df.columns.str.strip()
    area_struct_df.columns = area_struct_df.columns.str.strip()

    # area_category_df: 'category' 열을 int 타입으로 변환 (사용자 수정 반영)
    area_category_df['category'] = area_category_df['category'].astype(int)
    # area_category_df: 'struct' 열의 공백 제거 (사용자 수정 반영)
    area_category_df['struct'] = area_category_df['struct'].str.strip()

    # 데이터프레임 병합: area_struct_df와 area_category_df 병합
    merged_df = pd.merge(area_struct_df, area_category_df, on='category', how='left')

    # area_map_df (건설 현장 정보) 병합
    merged_df = pd.merge(merged_df, area_map_df, on=['x', 'y'], how='left')

    # category 0 (구조물 없음) 영역의 'struct' NaN 값 'Empty'로 채우기
    merged_df['struct'] = merged_df['struct'].fillna('Empty')

    # 셀의 최종 유형을 결정하는 함수
    def get_cell_type(row):
        # 건설 현장 우선순위 적용
        if row['ConstructionSite'] == 1:
            return 'ConstructionSite'
        elif row['struct'] == 'Apartment':
            return 'Apartment'
        elif row['struct'] == 'Building':
            return 'Building'
        elif row['struct'] == 'MyHome':
            return 'MyHome'
        elif row['struct'] == 'BandalgomCoffee':
            return 'BandalgomCoffee'
        else:
            return 'Empty'

    merged_df['final_type'] = merged_df.apply(get_cell_type, axis=1)

    return merged_df


# --- 2단계: 지도 시각화 함수 ---

def draw_map(df, file_name, path = None, start_node = None, end_node = None, show_legend = True):
    '''
    주어진 데이터프레임을 기반으로 지도를 시각화하여 이미지 파일로 저장합니다.

    Args:
        df (pandas.DataFrame): 지도에 표시할 데이터 (x, y, final_type 포함)
        file_name (str): 저장할 이미지 파일 이름 (예: 'map.png', 'map_final.png')
        path (list): (x, y) 튜플의 경로 리스트 (경로 시각화 시)
        start_node (tuple): 시작 노드의 (x, y) 좌표 (지도에 표시되지 않음)
        end_node (tuple): 끝 노드의 (x, y) 좌표 (지도에 표시되지 않음)
        show_legend (bool): 범례를 표시할지 여부
    '''
    max_x = df['x'].max()
    max_y = df['y'].max()

    plt.figure(figsize=(10, 10))
    ax = plt.gca()

    # 그리드 라인 설정 (numpy.arange 대신 list comprehension 사용)
    ax.set_xticks([x + 0.5 for x in range(max_x + 1)], minor = False)
    ax.set_yticks([y + 0.5 for y in range(max_y + 1)], minor = False)
    ax.grid(which = 'major', color = 'gray', linestyle = '-', linewidth = 0.5)

    # X축 눈금을 맵 위에 그리기
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    # 각 지점 플로팅
    # 범례 중복을 피하기 위해 사용
    unique_labels = {}
    for index, row in df.iterrows():
        x, y = row['x'], row['y']
        cell_type = row['final_type']

        if cell_type == 'Apartment' or cell_type == 'Building':
            label = 'Apartment/Building'
            if label not in unique_labels:
                plt.plot(x, y, 'o', color = 'saddlebrown', markersize = 20, label = label)
                unique_labels[label] = True
            else:
                plt.plot(x, y, 'o', color = 'saddlebrown', markersize = 20)
        elif cell_type == 'BandalgomCoffee':
            label = 'Bandalgom Coffee'
            if label not in unique_labels:
                plt.plot(x, y, 's', color = 'green', markersize = 20, label = label)
                unique_labels[label] = True
            else:
                plt.plot(x, y, 's', color = 'green', markersize = 20)
        elif cell_type == 'MyHome':
            label = 'My Home'
            if label not in unique_labels:
                plt.plot(x, y, '^', color = 'green', markersize = 20, label = label)
                unique_labels[label] = True
            else:
                plt.plot(x, y, '^', color = 'green', markersize = 20)
        elif cell_type == 'ConstructionSite':
            label = 'Construction Site'
            # 건설 현장은 바로 옆 좌표와 살짝 겹쳐도 되므로, 마커 크기를 약간 크게 설정
            if label not in unique_labels:
                plt.plot(x, y, 's', color = 'gray', markersize = 22, label = label)
                unique_labels[label] = True
            else:
                plt.plot(x, y, 's', color = 'gray', markersize = 22)

    # 경로 플로팅
    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        label = 'Shortest Path'
        if label not in unique_labels:
            plt.plot(path_x, path_y, color = 'red', linewidth = 2, marker = 'o', markersize = 5, label = label)
            unique_labels[label] = True
        else:
            plt.plot(path_x, path_y, color = 'red', linewidth = 2, marker = 'o', markersize = 5)

        # 시작점과 끝점 마커는 지도에서 제거


    plt.title('Area Map')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # X, Y 축 범위 설정 및 Y축 반전 ((1,1)이 좌측 상단이 되도록)
    plt.xlim(0.5, max_x + 0.5)
    plt.ylim(max_y + 0.5, 0.5)

    # 범례 표시 (지도 오른쪽 아래)
    # # 범례 표시 (지도 오른쪽 아래)

    legend_items = [
        plt.Rectangle((0, 0), 1, 1, facecolor='gray', alpha=0.7, 
                     edgecolor='black', linewidth=0.5, label='Construction Site'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='saddlebrown', 
                  markersize=12, markeredgecolor='black', markeredgewidth=0.5, 
                  label='Apartment / Building'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='darkgreen', 
                  markersize=12, markeredgecolor='black', markeredgewidth=0.5,
                  label='Bandalgom Coffee'),
        plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='limegreen', 
                  markersize=14, markeredgecolor='black', markeredgewidth=0.5,
                  label='My Home'),
    ]
    
    if path:
        legend_items.append(
            plt.Line2D([0], [0], color='red', linewidth=3, alpha=0.8, label='Shortest Path')
        )
    
    ax.legend(handles=legend_items, loc='lower right', frameon=True, 
             fancybox=True, shadow=True, fontsize=10)

    plt.xticks(list(range(1, max_x + 1)))
    plt.yticks(list(range(1, max_y + 1)))
    plt.gca().set_aspect('equal', adjustable = 'box')
    plt.savefig(file_name)
    plt.close()


# --- 3단계: 경로 탐색 및 메인 로직 ---

# _heuristic 함수는 BFS에서 사용되지 않으므로 제거합니다.

def _bfs_search(grid_width, grid_height, start, goal, impassable_cells):
    '''
    BFS (너비 우선 탐색) 알고리즘을 사용하여 그리드에서 시작점에서 목표점까지의 최단 경로를 찾습니다.
    이동 비용이 모두 1인 경우에 최단 경로를 보장하며, A*보다 간단합니다.
    Args:
        grid_width (int): 그리드의 최대 X 좌표
        grid_height (int): 그리드의 최대 Y 좌표
        start (tuple): 시작 노드의 (x, y) 좌표 (1-인덱스)
        goal (tuple): 목표 노드의 (x, y) 좌표 (1-인덱스)
        impassable_cells (set): 통과할 수 없는 (x, y) 튜플 집합
    Returns:
        list: (x, y) 튜플로 이루어진 최단 경로 리스트, 경로가 없으면 None
    '''
    if start in impassable_cells or goal in impassable_cells:
        return None # 시작점 또는 목표점이 통과 불가능한 지점인 경우

    # BFS를 위한 큐 (Python list의 pop(0) 사용)
    # collections.deque를 사용하면 더 효율적이지만, 외부 라이브러리 사용 제한으로 list 사용
    frontier = [start] 

    came_from = {start: None} # 경로 재구성을 위한 맵: {현재 노드: 이전 노드}
    g_cost = {start: 0} # 시작점에서 각 노드까지의 실제 비용 (BFS에서는 단계 수와 동일)

    while frontier:
        current = frontier.pop(0) # 큐의 가장 앞 노드 추출

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1] # 경로를 시작점에서 목표점 순서로 뒤집기

        # 가능한 이동 (상, 하, 좌, 우)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            # 이웃이 그리드 범위 내에 있는지 확인
            if not (1 <= neighbor[0] <= grid_width and 1 <= neighbor[1] <= grid_height):
                continue

            # 이웃이 통과 불가능한 지점인지 확인
            if neighbor in impassable_cells:
                continue

            # 이웃이 아직 방문되지 않은 경우 (g_cost에 없음)
            if neighbor not in g_cost:
                g_cost[neighbor] = g_cost[current] + 1
                frontier.append(neighbor)
                came_from[neighbor] = current
    return None # 경로를 찾을 수 없음

def find_closest_bandalgom_cafe(grid_width, grid_height, start_node, all_cafe_coords, impassable_cells):
    '''
    여러 반달곰 카페 중 시작점에서 가장 가까운 카페를 찾아 그 카페의 좌표와
    해당 카페까지의 최단 경로를 반환합니다. BFS를 사용합니다.
    Args:
        grid_width (int): 그리드의 최대 X 좌표
        grid_height (int): 그리드의 최대 Y 좌표
        start_node (tuple): 시작 노드의 (x, y) 좌표
        all_cafe_coords (list): 모든 반달곰 카페의 (x, y) 튜플 리스트
        impassable_cells (set): 통과할 수 없는 (x, y) 튜플 집합
    Returns:
        tuple: (가장 가까운 카페 좌표, 해당 카페까지의 최단 경로 리스트)
                경로를 찾을 수 없으면 (None, None) 반환
    '''
    min_path_length = float('inf')
    closest_cafe_node = None
    best_path_to_cafe = None

    for cafe_coord_arr in all_cafe_coords:
        cafe_node = tuple(cafe_coord_arr)
        # BFS를 사용하여 경로 탐색
        path_to_current_cafe = _bfs_search(grid_width, grid_height, start_node, cafe_node, impassable_cells)
        
        if path_to_current_cafe:
            current_path_length = len(path_to_current_cafe) - 1 # 단계 수
            if current_path_length < min_path_length:
                min_path_length = current_path_length
                closest_cafe_node = cafe_node
                best_path_to_cafe = path_to_current_cafe
    
    return closest_cafe_node, best_path_to_cafe


# --- 메인 실행 로직 ---
if __name__ == '__main__':
    # 데이터 로드 및 전처리
    merged_df = load_and_process_data('area_category.csv', 'area_map.csv', 'area_struct.csv')

    # 맵 크기(최대 x, y 좌표) 가져오기
    max_x = merged_df['x'].max()
    max_y = merged_df['y'].max()

    # 경로 탐색을 위한 통과 불가능한(건설 현장) 노드 집합 생성
    impassable_nodes = set()
    for index, row in merged_df[merged_df['final_type'] == 'ConstructionSite'].iterrows():
        impassable_nodes.add((row['x'], row['y']))

    # 초기 맵 저장 (경로 없음)
    draw_map(merged_df, 'map.png')

    # 내 집과 반달곰 커피 지점 좌표 찾기
    my_home_coords = merged_df[merged_df['final_type'] == 'MyHome'][['x', 'y']].values
    bandalgom_coffee_coords = merged_df[merged_df['final_type'] == 'BandalgomCoffee'][['x', 'y']].values

    if len(my_home_coords) == 0:
        print('Error: MyHome not found on the map.')
        exit()
    if len(bandalgom_coffee_coords) == 0:
        print('Error: Bandalgom Coffee not found on the map.')
        exit()

    start_node = tuple(my_home_coords[0])
    
    print(f'My Home (시작점): {start_node}')
    print(f'모든 반달곰 커피 지점: {[tuple(c) for c in bandalgom_coffee_coords]}')

    # 가장 가까운 반달곰 커피 지점 찾기 및 최단 경로 계산
    end_node, final_path = find_closest_bandalgom_cafe(
        max_x, max_y, start_node, bandalgom_coffee_coords, impassable_nodes
    )
    
    if end_node:
        print(f'가장 가까운 반달곰 커피 (도착점): {end_node}')
        print(f'최단 경로 길이: {len(final_path) - 1} 단계')
        # 경로를 CSV로 저장
        path_df = pd.DataFrame(final_path, columns=['x', 'y'])
        path_df.to_csv('home_to_cafe.csv', index=False)
        print('home_to_cafe.csv 파일이 저장되었습니다.')

        # 경로가 표시된 최종 맵 그리기
        draw_map(merged_df, 'map_final.png', path = final_path, start_node = start_node, end_node = end_node)
        print('map_final.png 파일이 저장되었습니다.')
    else:
        print('가장 가까운 반달곰 커피 지점까지의 경로를 찾을 수 없습니다.')
        # 경로를 찾을 수 없는 경우, 경로가 없는 최종 맵 다시 그리기
        draw_map(merged_df, 'map_final.png')
        print('map_final.png 파일이 저장되었습니다 (경로 없음).')