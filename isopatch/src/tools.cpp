#include <stdio.h>
#include <stdlib.h>
#include <io.h>
#include <fcntl.h>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>


int dump_bin(char *filename, char *pBuf, int nBytesToWrite)
{
	/*
		//ﾕ籔ﾖﾐｴﾓﾐｸug, ｾﾍﾊﾇﾐｴﾈ・Dｻ瞹ﾔｶｯﾔﾚｺ貍ﾓｸ・A｣ｬｾﾍﾏﾄｱｾﾄ｣ﾊｽｴｪﾒｻﾑ・
		int fhTemp;
		fhTemp = _creat(filename, _O_BINARY | _O_WRONLY | _S_IREAD | _S_IWRITE );
		if(fhTemp == -1) return -1;

		nBytesToWrite = _write(fhTemp, pBuf, nBytesToWrite);
		_close(fhTemp);
		return nBytesToWrite;
	*/
	FILE *fp;
	fp = fopen(filename, "wbc");
	if(fp == NULL) return -1;
	nBytesToWrite = fwrite(pBuf, nBytesToWrite, 1, fp);
	fflush(fp);
	fclose(fp);
	return nBytesToWrite;
}
int load_bin(char *filename, char *pBuf, int nBuffer)
{
	int fhTemp;
	int nFileLen;

	fhTemp = _open(filename, _O_BINARY | _O_RDONLY);
	if(fhTemp == -1) return -1;
	nFileLen = filelength(fhTemp);
	if(nFileLen > nBuffer) {return -1; _close(fhTemp); }

	_read(fhTemp, pBuf, nFileLen);
	_close(fhTemp);
	return nFileLen;
}


int HexStr2Byte(char *pString, char *buf, int buf_len)
{
	int len;
	int convert_len;

	char buf_byte[3];
	int b;
	char buf_tmp[16];
	

	len = strlen(pString);
	if(len % 2 != 0)return -1;

	convert_len = 0;
	for(int i=0;i<len;i+=2)
	{
		buf_byte[0] = pString[i];
		buf_byte[1] = pString[i+1];
		buf_byte[2] = 0;

		sscanf(buf_byte, "%x", &b);
		sprintf(buf_tmp, "%02X", b);
		if(lstrcmpi(buf_tmp, buf_byte) != 0)return -2;

		buf[convert_len] = b;

		convert_len++;
	}

	return convert_len;
}
int get_filelen(char *filename)
{
	int fhTemp;
	int nFileLen;

	fhTemp = _open(filename, _O_BINARY | _O_RDONLY);
	if(fhTemp == -1) return -1;
	nFileLen = filelength(fhTemp);
	_close(fhTemp);
	return nFileLen;
}

int get_path(char *path_old, char *path_new, int path_new_len)
{
	int i;
	memset(path_new, 0, path_new_len);

	for(i=lstrlen(path_old)-1;i>=0;i--)
	{
		if(path_old[i] == '\\')
		{
			memcpy(path_new, path_old, i+1);
			return i;
		}
	}

	return 0;
}


void MyTrace(const char *fmt, ...)
{
	//ﾍｬﾊｱﾔﾚVC Outputｴｰｿﾚﾏﾔﾊｾﾐﾅﾏ｢, ﾒｻｰ飜ﾇｵﾔﾐﾅﾏ｢
	//ﾈ郢﨣默・ﾄﾊﾇDLLｰ誄rintf, OutputDebugString ｶｼﾎﾞｲｻｻ睫莎ｬﾃｻﾊﾂ｡｣ｲｻﾓﾃｹﾜﾋ・｣
	char txt[8024];
	va_list		ap;

	if (fmt == NULL)return;			// Do Nothing

	ZeroMemory(txt, sizeof(txt));
	va_start(ap, fmt);
	    vsprintf(txt, fmt, ap);
	va_end(ap);
	
	printf("%s", txt);
	OutputDebugString(txt);
}
