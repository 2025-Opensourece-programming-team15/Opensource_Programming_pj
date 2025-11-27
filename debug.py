import pandas as pd
import sys
import os

# 모듈 경로 설정 (src 폴더 인식을 위해 필요할 수 있음)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 1. 통합 검색 함수 임포트
# 실제 크롤러 작동 확인을 위해 예외 처리(try-except)와 더미 함수를 제거했습니다.
# 이제 모듈 임포트에 실패하면 프로그램이 에러를 발생시키고 종료됩니다.
from src.crawler_wrapper import search_community

def test_gallery_search(gallery_id: str, gallery_type: str, keyword: str, search_option: int = 0, end_page: int = 1):
    """
    DC 갤러리 검색 테스트 (search_community 사용)
    """
    print(f"\n--- [테스트 시작] 갤러리 검색 (Via search_community) ---")
    print(f"대상: DC, 갤러리: {gallery_id}, 타입: {gallery_type}, 키워드: '{keyword}'")
    
    # 통합 함수 호출 (target_source='dc' + gallery_id 포함)
    results_df = search_community(
        target_source='dc',
        keyword=keyword,
        start_page=1,
        end_page=end_page,
        # **kwargs로 전달될 옵션들
        gallery_id=gallery_id,
        gallery_type=gallery_type,
        search_option=search_option
    )
    
    _print_results(results_df, f"test_GALLERY_{gallery_id}_{keyword[:10]}")


def test_integrated_search(keyword: str, sort_type: str = "latest", end_page: int = 1):
    """
    DC 통합 검색 테스트 (search_community 사용)
    """
    print(f"\n--- [테스트 시작] 통합 검색 (Via search_community) ---")
    print(f"대상: DC, 키워드: '{keyword}', 정렬: {sort_type}")
    
    # 통합 함수 호출 (target_source='dc' + gallery_id 없음 -> 통합 검색으로 라우팅됨)
    results_df = search_community(
        target_source='dc',
        keyword=keyword,
        start_page=1,
        end_page=end_page,
        # **kwargs
        sort_type=sort_type
    )
    
    _print_results(results_df, f"test_INTEGRATED_{keyword[:10]}_{sort_type}")


def test_arca_search(keyword: str, channel_id: str = 'breaking', end_page: int = 1):
    """
    아카라이브 검색 테스트 (search_community 사용)
    """
    print(f"\n--- [테스트 시작] 아카라이브 검색 (Via search_community) ---")
    print(f"대상: Arca, 채널: {channel_id}, 키워드: '{keyword}'")
    
    # 통합 함수 호출 (target_source='arca')
    results_df = search_community(
        target_source='arca',
        keyword=keyword,
        start_page=1,
        end_page=end_page,
        # **kwargs
        channel_id=channel_id
    )
    
    _print_results(results_df, f"test_ARCA_{channel_id}_{keyword[:10]}")


def _print_results(df: pd.DataFrame, file_prefix: str):
    """결과 출력 및 저장 헬퍼 함수"""
    if df.empty:
        print("➡️ 수집된 게시물이 없거나 요청에 실패했습니다.")
    else:
        print(f"✅ 최종 수집된 게시물 수: {len(df)}개")
        print("\n--- 결과 DataFrame (상위 5개) ---")
        print(df.head())
        
        # CSV 파일로 저장
        file_name = f"{file_prefix}.csv"
        try:
            df.to_csv(file_name, index=False, encoding="utf-8-sig")
            print(f"\n💾 데이터가 {file_name} 파일로 저장되었습니다.")
        except Exception as e:
            print(f"\n⚠️ 파일 저장 실패: {e}")


def run_all_tests():
    """대화형 테스트 실행 루프"""
    print("=================================================")
    print("   통합 검색 인터페이스(search_community) 디버거")
    print("=================================================")
    
    while True:
        try:
            print("\n--------------------------------")
            choice = input("테스트할 기능 선택 (1: DC 갤러리, 2: DC 통합, 3: Arca 채널, 0: 종료): ")
            choice = int(choice.strip())
        except ValueError:
            print("❗ 숫자를 입력해주세요.")
            continue
            
        if choice == 0:
            print("\n테스트 프로그램을 종료합니다.")
            break

        try:
            if choice == 1:
                # DC 갤러리 검색
                print("\n[설정] DC 갤러리 검색")
                gall = input("갤러리 ID (ex: programming): ").strip()
                gall_type = input("갤러리 타입 (major/minor/mini) [Enter=minor]: ").strip() or "minor"
                keyword = input("키워드: ").strip()
                
                opt = input("검색 옵션 (0:전체, 1:제목, 2:내용) [Enter=0]: ").strip() or "0"
                page = input("페이지 수 [Enter=1]: ").strip() or "1"
                
                test_gallery_search(
                    gallery_id=gall, 
                    gallery_type=gall_type, 
                    keyword=keyword, 
                    search_option=int(opt), 
                    end_page=int(page)
                )
            
            elif choice == 2:
                # DC 통합 검색
                print("\n[설정] DC 통합 검색")
                keyword = input("키워드: ").strip()
                sort_in = input("정렬 (1:최신순, 2:정확도순) [Enter=1]: ").strip()
                sort_type = 'accuracy' if sort_in == '2' else 'latest'
                page = input("페이지 수 [Enter=1]: ").strip() or "1"
                
                test_integrated_search(
                    keyword=keyword, 
                    sort_type=sort_type, 
                    end_page=int(page)
                )
                
            elif choice == 3:
                # Arca 검색
                print("\n[설정] ArcaLive 검색")
                print("(팁: 통합검색은 채널ID에 'breaking' 입력 [Enter=breaking])")
                channel = input("채널 ID (ex: genshin): ").strip() or "breaking"
                keyword = input("키워드: ").strip()
                page = input("페이지 수 [Enter=1]: ").strip() or "1"
                
                test_arca_search(
                    channel_id=channel, 
                    keyword=keyword, 
                    end_page=int(page)
                )
                
            else:
                print("⚠️ 올바른 번호를 선택해주세요.")
                
        except ValueError as e:
            print(f"❗ 입력값 오류: 정수를 입력해야 하는 곳에 문자가 입력되었거나 잘못된 값입니다. ({e})")
        except Exception as e:
            print(f"🚨 실행 중 예기치 않은 오류 발생: {e}")

if __name__ == '__main__':
    run_all_tests()