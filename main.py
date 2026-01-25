import time
import os
import requests
import argparse
from urllib.parse import urlparse

def get_filename_from_response(response, url):
    cd = response.headers.get("content-disposition")

    # 1. Try with header
    if cd:
        parts = cd.split("filename=")
        if len(parts) > 1:
            return parts[1].strip().strip('"')
        
    # 2.Try with URL
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    if filename: return filename

    # 3. If none matches then return by default
    return "Download_File"

def print_progress(downloaded, total_size, start_time, bar_length = 30):
    elapsed = time.time() - start_time
    speed = downloaded / elapsed if elapsed > 0 else 0
    speed_mb = speed / (1024 * 1024)

    if total_size > 0 :
        percent = downloaded / total_size
        filled = int(bar_length * percent)
        bar = "█" * filled + "░" * (bar_length - filled)

        remaining = total_size - downloaded
        eta = remaining / speed if speed > 0 else 0

        print(
            f"\r[{bar}] {percent * 100 : 5.1f}% | ",
            f"{speed_mb : .2f} MB/s | ",
            f"ETA: {int(eta)}s", 
            end="", 
            flush=True
        )

    else :
        print(
            f"Downloaded : {downloaded / (1024 * 1024) : .2f} MB ",
            f"{speed_mb : .2f}",
            end="",
            flush=True
        )

    return


def download_file(url, file_name):
    try : 
        response = requests.get(url=url, stream= True, timeout=10)



        # calls method for storing the file name
        if not file_name:
            file_name = get_filename_from_response(response, url)

        resume_byte_pos = 0
        if file_name and os.path.exists(file_name):
            resume_byte_pos = os.path.getsize(file_name)

        headers = {}
        if resume_byte_pos > 0 :
            headers["Range"] = f"bytes={resume_byte_pos}-"
            print(f"Resuming download from {resume_byte_pos} byte")

        response = requests.get(url=url, stream= True, headers= headers, timeout=10)

        # checks the status response

        # 200 - server successfully proceeds the request and returned successfully
        # 206 - server returns only the part of content where you specified the range 
        if (response.status_code != 200)  and (response.status_code != 206):   # if status check fails then it print invalid msg and send the status code
            if response.status_code == 416:
                print("Not possible range or file can be already downloaded")  

                is_continue = True if input("Do you want to delete and download again 'y'|| 'Y' : ") in ['y', 'Y'] else False
                if is_continue: 
                    print("Removing file from path : ")
                    os.remove(file_name)
                    print(" ---File removed ")
                    print(" ---File starts downloading")
                    download_file(url, None)

                else:
                    print("You don't want to delete the existing file right ? ")
                return     

            print(f"Invalid : {response.status_code}")
            return 

        # calculate the size of the file
        total_size = int(response.headers.get("content-length", 0))
        
        if response.status_code == 206:
            total_size += resume_byte_pos
        downloaded = resume_byte_pos # initially downloaded

        # opens file with returned file name to overwrite the content
        mode = "ab" if resume_byte_pos > 0 else "wb"
        with open(file_name, mode) as file:    
            start_time = time.time()                         # if the file not present it creates by the name or it will overwrite the previous one
            for chunk in response.iter_content(chunk_size=1024):        # get chunks from the response
                if not chunk: continue

                file.write(chunk)                                       # write the data in the file

                if total_size == 0:                                     # handle data if the file size is unknown
                    downloaded = downloaded / (1024 * 1024)
                    print(f"\rDownloaded : {downloaded} %",end = "", flush= True) # flush the command line for every time

                else:                                                   # handles if the file size is known
                    downloaded += len(chunk)
                    print_progress(downloaded, total_size, start_time)
                    # time.sleep()                                    # used when user needs to see the download process clearly

        print("\n -------------- DONE --------------")
    
    except requests.exceptions.Timeout:
        print("Error : Time out")

    except requests.exceptions.RequestException as e:
        print(f"Error : {e}")


def main():
    parser = argparse.ArgumentParser(description= "Simple arg parser")

    # parse the data given through command line so it feels like the user input
    parser.add_argument("url", 
                        help= "give a url link here to download")
    
    # if user gives output file name in command it will accept 
    parser.add_argument( '-o', "--output",
                        default= None,                               # by default it set as None, no data is also allowed
                        help= "output file name")
    
    args = parser.parse_args()

    download_file(args.url, args.output)                             # pass the url and output file name


if __name__ == "__main__" : 
    main()