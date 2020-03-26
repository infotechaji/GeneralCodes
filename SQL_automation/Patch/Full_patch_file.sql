
/*$File_version=MS4.3.0.00$*/
/********************************************************************************************/
/*	Filename				:	xxx-1111.sql											        */
/*	Author					:	AAAAAAAAA B													    */
/*	Date					:	01/01/2020														*/
/*	Component name			:																	*/
/*	DTSID					:	xxx-1111														*/
/*	Purpose of Patch		:	Table Script													*/
/********************************************************************************************/

SET NOCOUNT  ON
			
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_anti_cap_ethu'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_anti_cap_ethu  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_rem_cap_qty'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_rem_cap_qty  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_blocked_sa_ml'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_blocked_sa_ml  udd_desc255  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_rem_cap_ci'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_rem_cap_ci  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_blocking_reason_ml'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_blocking_reason_ml  udd_desc40  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_rem_cap_ethu'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_rem_cap_ethu  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_anti_cap_ci'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_anti_cap_ci  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_blocked_pick_ml'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_blocked_pick_ml  udd_desc255  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_rem_cap_vol'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_rem_cap_vol  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_rem_cap_wgt'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_rem_cap_wgt  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_blocked_pawy_ml'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_blocked_pawy_ml  udd_desc255  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_anti_cap_wgt'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_anti_cap_wgt  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_bin_checkbit_ml'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_bin_checkbit_ml  udd_desc40  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_anti_cap_qty'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_anti_cap_qty  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_anti_cap_vol'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_anti_cap_vol  udd_quantity  null
	END
		
	IF NOT EXISTS 
		(
		SELECT	'X'
		FROM	sysobjects		a (NOLOCK),
				syscolumns		b (NOLOCK)
		WHERE	a.id		=	b.id
		AND		a.name      =	'wms_bin_dtl'
		AND		b.name      =	'wms_bin_bin_full_ml'
		AND		a.type      =	'U'
		)
	BEGIN
		ALTER TABLE wms_bin_dtl ADD wms_bin_bin_full_ml  udd_desc255 null
	END
		
SET NOCOUNT  OFF
			