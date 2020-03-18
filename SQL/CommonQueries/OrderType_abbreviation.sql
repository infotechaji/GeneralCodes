-- description for the order types 
	 	
		
		IF @Refdoctype_Tmp = 'PO'
		BEGIN
				SELECT @refdocsubtype_desc = POPRM_PARAMDESC
				FROM   PO_POPRM_PARAMETER_DETAILS WITH(NOLOCK)
				WHERE  POPRM_COMPONENTNAME = 'BASPO'
				AND    POPRM_PARAMCATEGORY = 'COMBO'
				AND    POPRM_PARAMTYPE     = 'POTYPE'
				AND    POPRM_PARAMCODE     = @refdocsubtype
		END
		
		IF @Refdoctype_Tmp = 'RS'
		BEGIN
				SELECT @refdocsubtype_desc = CASE @refdocsubtype WHEN 'N' THEN 'NORMAL' 
												  ELSE 'EXPRESS' END
		END
		
		
		IF @Refdoctype_Tmp = 'RO'
		BEGIN
				SELECT @refdocsubtype_desc = REPPRM_PARAMDESC
				FROM   REP_REPPRM_PARAMETER_DTL WITH(NOLOCK)
				WHERE  REPPRM_COMPONENTNAME = 'BASREPAIRORDER'
				AND    REPPRM_PARAMCATEGORY = 'COMBO'
				AND    REPPRM_PARAMTYPE     = 'ROTYPE'
				AND    REPPRM_PARAMCODE		= @refdocsubtype
		END
		
		IF @Refdoctype_Tmp = 'CO'
		BEGIN 
			SELECT @refdocsubtype_desc = CASE @refdocsubtype WHEN 'PIP' THEN 'Piece Part'
															 WHEN 'COM' THEN 'Component'
															 WHEN 'PRO' THEN 'Project'
															 WHEN 'MAK' THEN 'Make'
															 WHEN 'MSC'	THEN 'Miscellaneous'
															 WHEN 'E'	THEN 'Engine'
															 ELSE '' END
		END