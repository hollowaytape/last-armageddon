#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <io.h>
#include <fcntl.h>
#define WIN32_LEAN_AND_MEAN		// ´Ó Windows Í·ÖĞÅÅ³ıÒ»Ğ©²»³£Ê¹ÓÃµÄ²¿·Ö£¬ÈçGDI
#include <windows.h>

#include "ecc_edc.h"
#include "tools.h"
#include "iso9660.h"


#define PATCH_ERR_FILE_ISO		-1
#define PATCH_ERR_FILE_PATCH	-2
#define PATCH_ERR_FILE_PATCHLST	-3
#define PATCH_ERR_OFFSET		-4
#define PATCH_ERR_TEMPFILE		-5
#define PATCH_ERR_BYTES			-6
#define PATCH_ERR_LINETOOLONG	-7
#define PATCH_ERR_UNK_COMMAND	-8
#define PATCH_ERR_UNK_MODE		-9
#define PATCH_ERR_DIRECT		-10

char *error_string[] = 
{
	"no error",
	"can't access ISO file",
	"can't access patch file",
	"can't access patch list file",
	"start offset is incorrect",
	"can't create temp file",
	"raw bytes is incorrect",
	"patch line too long",
	"unknown command",
	"unknown iso mode",
	"direct mode err"
};

//iso_offset 32bitÕûÊı¡£ÄÜ±úæ¾µÄÊı×Ö×ûĞóÔ¼0x80000000£¬Õâ¸ö×ã¹»±úæ¾isoµÄ£¬iso9660Ò»°ã×ûÒEx2???????
//Èç¹û»»³É64bit´óÕûÊı£¬vbµ÷ÓÃÆğÀ´¾ÍÂÔÂé·³ÁË£¬Ò²ÔİÊ±Ã»±ØÒª¡£
//º¯Êı·µ»ØpatchµÄ×Ö½ÚÊı¡£Èç¹û´úêó·µ»Ø¸ºÊı£¬Îª¸÷ÖÖ¿ÉÄÜµÄ³£Á¿¡£
int WINAPI iso_patch_file(int iso_type, char *iso_file, int need_ecc_edc, int iso_offset, char *patch_file)
{
	int fhISO, fhPatch;
	int sector_start;
	int sector_length;
	BYTE sector[2352];

	//**** ³õÊ¼»¯£«ºÏ·¨ĞÔ¼EE ²»ºÏ·¨·µ»Ø´úêE
	if (iso_offset <= 0) return PATCH_ERR_OFFSET;
	sector_start = iso_offset % 2352;
	if(sector_start < ISO9660_DATA_START[iso_type] || sector_start >= ISO9660_DATA_START[iso_type]+ISO9660_DATA_SIZE[iso_type]) return PATCH_ERR_OFFSET;

	fhPatch = _open(patch_file, _O_BINARY | _O_RDONLY);
	if(fhPatch == -1){ return PATCH_ERR_FILE_PATCH;}

	fhISO = _open(iso_file, _O_BINARY | _O_RDWR);
	if(fhISO == -1){ _close(fhPatch); return PATCH_ERR_FILE_ISO;}

	sector_length = ISO9660_DATA_SIZE[iso_type] +  ISO9660_DATA_START[iso_type] - sector_start;

	eccedc_init();

	//**** Ğ´ÈE
	int total_patched_bytes = 0;
	int size_read;
	int nTmp;
	nTmp = iso_offset - (iso_offset % 2352);

	_lseek(fhISO, nTmp, SEEK_SET);

	
	for (;_eof(fhPatch)==0;)
	{
		
		_read(fhISO,sector,2352);								//¶ÁÈEªĞŞ¸ÄµÄÉÈÇøÊı¾İµ½»º³E
		size_read = _read(fhPatch,
						&sector[sector_start],
						sector_length);			//ĞŞ¸Ä»º³E
		
		//if ((sector[0x12] & 8) == 0)
		//{
		//	//¼EâÊÇ·ñÊÇÊı¾İÉÈÇø£¬Èç¹ûÊÇĞ´ÔÚleadoutµÈÇø¶Î£¬Ò²×Ô¶¯¸ÄÎªÊı¾İÉÈÇø¸ñÊ½
		//	sector[0x12] = 8;
		//	sector[0x16] = 8;
		//}

		if (need_ecc_edc != 0)eccedc_generate(sector, iso_type);//ÖØËEEDC/ECC

		_lseek(fhISO, -2352, SEEK_CUR);							//ÉèÖÃ ISO ÎÄ¼şÖ¸ÕEµ»Øµ½ÉÈÇø¿ªÊ¼´¦
		_write(fhISO, sector, 2352);							//Ğ´ÈEŞ¸ÄºóµÄÉÈÇøÊı¾İ
		total_patched_bytes += size_read;						//Ò»¸Epatch Êı¾İÎÄ¼şÊµ¼ÊĞ´ÈEÖ½ÚÊı¼ÆÊı
		sector_start = ISO9660_DATA_START[iso_type];
		sector_length = ISO9660_DATA_SIZE[iso_type];
	}

	_close(fhPatch);
	_close(fhISO);

	return total_patched_bytes;
}

int WINAPI iso_patch_sector(char *iso_file, int iso_offset, char *patch_file)
{
	int fhISO, fhPatch;

	//**** ³õÊ¼»¯£«ºÏ·¨ĞÔ¼EE ²»ºÏ·¨·µ»Ø´úêE
	if (iso_offset <= 0) return PATCH_ERR_OFFSET;

	fhPatch = _open(patch_file, _O_BINARY | _O_RDONLY);
	if(fhPatch == -1){ return PATCH_ERR_FILE_PATCH;}

	fhISO = _open(iso_file, _O_BINARY | _O_RDWR);
	if(fhISO == -1){ _close(fhPatch); return PATCH_ERR_FILE_ISO;}

	//**** Ğ´ÈE
	int total_patched_bytes = 0;


	static char buff[1024*1024];
	int nBuff;
	_lseek(fhPatch, 0, SEEK_END);
	nBuff = _tell(fhPatch);
	_lseek(fhPatch, 0, SEEK_SET);
	if(nBuff > sizeof(buff)) return PATCH_ERR_DIRECT;
	_read(fhPatch,buff,nBuff);

	_lseek(fhISO, iso_offset, SEEK_SET);
	_write(fhISO, buff, nBuff);							//Ğ´ÈEŞ¸ÄºóµÄÉÈÇøÊı¾İ
	total_patched_bytes += nBuff;						//Ò»¸Epatch Êı¾İÎÄ¼şÊµ¼ÊĞ´ÈEÖ½ÚÊı¼ÆÊı

	_close(fhPatch);
	_close(fhISO);

	return total_patched_bytes;
}


int WINAPI iso_patch_byte(int iso_type, char *iso_file, int need_ecc_edc, int iso_offset, char *patch_buf, int patch_bytes)
{
	int nRet;
	char *pTmpFile = "$$$patch.$$$";
	nRet = dump_bin(pTmpFile, patch_buf, patch_bytes);
	if (nRet < 0) return PATCH_ERR_TEMPFILE;

	nRet = iso_patch_file(iso_type, iso_file, need_ecc_edc, iso_offset, pTmpFile);
	_unlink(pTmpFile);

	return nRet;
}

int iso_patch_list_core(int iso_type, char *iso_file, int need_ecc_edc, char *patch_list_file, int isTestMode, int *ErrorLine)
{
	#define MAX_PATCH_BYTE	32*1024				//Ò»ĞĞÖ±½ÓĞ´ÈEÄ×Ö½Ú×ûÒàÊÇ¶àÉÙ×Ö½Ú
	#define MAX_FILENAME	1024
	#define MAX_LINE		MAX_PATCH_BYTE+10	//Ò»ĞĞ×ûÒàÊÇ¶àÉÙ×Ö½Ú
	char buf_line[MAX_LINE];
	char buf_byte[MAX_PATCH_BYTE];				//Ö±½ÓĞ´ÈEÄ×Ö½Ú
	char patch_file[MAX_FILENAME];
	int  buf_byte_len;
	char buf_tmp[1024];
	char *off, *param;
	int iso_offset;
	int data_type;
	int patch_bytes_current, patch_bytes_total;

	FILE *fp;
	fp = fopen(patch_list_file, "r");
	if (fp == NULL) return PATCH_ERR_FILE_PATCHLST;
	*ErrorLine = 1;
	patch_bytes_total = 0;

	MyTrace("Mode         : ");
	if (iso_type == ISO9660_M1)
		MyTrace("MODE1\n");
	else if(iso_type == ISO9660_M2F1)
		MyTrace("MODE2 FORM1\n");
	else if(iso_type == ISO9660_M2F2)
		MyTrace("MODE2 FORM2\n");
	else
	{
		MyTrace("bad mode %d\n", iso_type);
		return PATCH_ERR_UNK_MODE;
	}
	MyTrace("ECC/EDC calc : ");
	if(need_ecc_edc)
		MyTrace("on\n");
	else
		MyTrace("off\n");

    MyTrace("list file    : %s\n", patch_list_file);
	MyTrace("iso  file    : %s\n", iso_file);
	MyTrace("\n");

	if(isTestMode)
		MyTrace("loading  list ...\n");
	else
		MyTrace("patching list ...\n");


	MyTrace("-----------------------------------------------------------------------------\n");
	MyTrace("line | offset   <- data      \t| length    \n");
	MyTrace("-----------------------------------------------------------------------------\n");

	for(;;*ErrorLine = *ErrorLine + 1)
	{
		if(feof(fp))break;
		memset(buf_line, 0, sizeof(buf_line));
		fgets(buf_line, MAX_LINE-1, fp);

		if( lstrlen(buf_line) >= MAX_LINE-1) return PATCH_ERR_LINETOOLONG;
		if(buf_line[lstrlen(buf_line)-1] == 0x0a) buf_line[lstrlen(buf_line)-1] = 0;

		if(buf_line[0] == 0)continue;
		if(buf_line[0] == ';')continue;
		if(buf_line[0] == '#')continue;

		data_type = 0;
		if(buf_line[8] == ',')data_type = 1;
		if(buf_line[8] == '*')data_type = 2;
		if(buf_line[8] == '@')data_type = 3;	//Ö±½ÓĞ´ÈEAW 2352ÉÈÇE
		if (data_type == 0) return PATCH_ERR_UNK_COMMAND;

		buf_line[8] = 0;	//ĞÎ³Éoff×Ö·û´®
		off = buf_line;
		param = buf_line + 8 + 1;
		sscanf(off, "%x", &iso_offset);
		sprintf(buf_tmp, "%08X", iso_offset);
 		if(lstrcmpi(buf_tmp, off) != 0)
		{
			fclose(fp);
			return PATCH_ERR_OFFSET;
		}
		if (iso_offset <= 0) return PATCH_ERR_OFFSET;
		int sector_start = iso_offset % 2352;
		if(data_type != 3)
			if(sector_start < ISO9660_DATA_START[iso_type] || sector_start >= ISO9660_DATA_START[iso_type]+ISO9660_DATA_SIZE[iso_type]) return PATCH_ERR_OFFSET;

		if(data_type == 1)	//ÃEûĞ¦ÀE
		{
			get_path(patch_list_file, buf_tmp, sizeof(buf_tmp));
			sprintf(patch_file, "%s%s", buf_tmp, param);

			if(isTestMode)
			{
				MyTrace("%4d | %08X", *ErrorLine, iso_offset);
				MyTrace(" <- %s", param);
				patch_bytes_current = get_filelen(patch_file);
			}
			else
			{
				MyTrace("%4d | %08X", *ErrorLine, iso_offset);
				MyTrace(" <- %s ...", param);
				patch_bytes_current = iso_patch_file(iso_type, iso_file, need_ecc_edc, iso_offset, patch_file);
				if (patch_bytes_current < 0) return patch_bytes_current;
				patch_bytes_total += patch_bytes_current;
			}

		}
		else if (data_type == 2)
		{
			memset(buf_byte, 0, sizeof(buf_byte));
			buf_byte_len = HexStr2Byte(param, buf_byte, sizeof(buf_byte));
			if(buf_byte_len < 0) return PATCH_ERR_BYTES;

			if(isTestMode)
			{
				MyTrace("%4d | %08X", *ErrorLine, iso_offset);
				MyTrace(" <- hex string   ");
				patch_bytes_current = buf_byte_len;
			}
			else
			{
				MyTrace("%4d | %08X", *ErrorLine, iso_offset);
				MyTrace(" <- hex string ...");
				patch_bytes_current = iso_patch_byte(iso_type, iso_file, need_ecc_edc, iso_offset, buf_byte, buf_byte_len);
				if (patch_bytes_current < 0) return patch_bytes_current;
				patch_bytes_total += patch_bytes_current;
			}

		}
		else
		{
			get_path(patch_list_file, buf_tmp, sizeof(buf_tmp));
			sprintf(patch_file, "%s%s", buf_tmp, param);

			if(isTestMode)
			{
				MyTrace("%4d | %08X", *ErrorLine, iso_offset);
				MyTrace(" <-RAW %s", param);
				patch_bytes_current = get_filelen(patch_file);
			}
			else
			{
				MyTrace("%4d | %08X", *ErrorLine, iso_offset);
				MyTrace(" <-RAW %s ...", param);
				patch_bytes_current = iso_patch_sector(iso_file, iso_offset, patch_file);
				if (patch_bytes_current < 0) return patch_bytes_current;
				patch_bytes_total += patch_bytes_current;
			}

		}
		
		MyTrace("\t| %d\n", patch_bytes_current);
	}

	fclose(fp);
	*ErrorLine = 0;
	return patch_bytes_total;
}
int WINAPI iso_patch_list(int iso_type, char *iso_file, int need_ecc_edc, char *patch_list_file)
{

	int nRet;
	int nErrLine = 0;

	//ÏÈÄ£ÄâĞ´ÈE¬²âÊÔºÏ·¨ĞÔ
	nRet = iso_patch_list_core(iso_type, iso_file, need_ecc_edc, patch_list_file, 1, &nErrLine);
	if (nRet < 0)
	{
		MyTrace("%4d | error(%d) %s\n", nErrLine, nRet, error_string[abs(nRet)] );
		return nRet;
	}
	
	MyTrace("-----------------------------------------------------------------------------\n");
	MyTrace("Press any key to start patching, press CTRL+BREAK to abort.");
	getch();
	MyTrace("\n");

	//È«²¿ºÏ·¨ÁËÒÔºóÕæÊµĞ´ÈE
	nRet = iso_patch_list_core(iso_type, iso_file, need_ecc_edc, patch_list_file, 0, &nErrLine);
	if (nRet < 0)
	{
		MyTrace("%4d | error(%d) %s\n", nErrLine, nRet, error_string[abs(nRet)] );
		return nRet;
	}

	MyTrace("-----------------------------------------------------------------------------\n");
	return nRet;
}

