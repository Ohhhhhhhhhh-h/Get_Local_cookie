# Get Local Cookie by chrome webdrive-80.0.3987.87

This script can read the cookie file generated locally by chrome and output all cookies of the required website

To avoid conflicts with the browser when connecting to the database, the script will generate a subdirectory named Local in the directory where it is located, and copy the cookie file to the directory for reading

Step:

    from Get_local_cookie import get_local_cookie

      cookie = get_local_cookie(your url)
