USE [Gestion]
GO
/****** Object:  StoredProcedure [dbo].[AntoUpdate_Proveedores]    Script Date: 30/03/2026 10:49:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[AntoUpdate_Proveedores]
    @RAZON_SOCIAL VARCHAR(200),
    @CUIL CHAR(11),
    @PROVINCIA VARCHAR(50),
    @LOCALIDAD VARCHAR(50),
    @CALLE VARCHAR(50),
    @CALLE_NRO CHAR(6),
    @DPTO VARCHAR(50),
    @PISO VARCHAR(50),
    @EMAIL VARCHAR(50),
    @CONDICION_CTA VARCHAR(30),
    @CONDICION_EN_AFIP VARCHAR(30),
    @CONDICION_DGR VARCHAR(30),
    @CONDICION_GCIA VARCHAR(30),
    @CONDICION_EMPLEADOR VARCHAR(30),
    @FORMA_JURIDICA VARCHAR(80),
    @FECHA_ULT_LIB_DEUDA DATETIME = NULL,
    @DNI_DESDE_CUIT INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Actualización de los datos
    UPDATE PROVEEDORES 
    SET 
        RAZON_SOCIAL = @RAZON_SOCIAL,
        PROVINCIA = @PROVINCIA,
        LOCALIDAD = @LOCALIDAD,
        CALLE = @CALLE,
        CALLE_NRO = @CALLE_NRO,
        DPTO = @DPTO,
        PISO = @PISO,
        EMAIL = @EMAIL,
        CONDICION_CTA = @CONDICION_CTA,
        CONDICION_EN_AFIP = @CONDICION_EN_AFIP,
        CONDICION_DGR = @CONDICION_DGR,
        CONDICION_GCIA = @CONDICION_GCIA,
        CONDICION_EMPLEADOR = @CONDICION_EMPLEADOR,
        FORMA_JURIDICA = @FORMA_JURIDICA,
        FECHA_ULT_LIB_DEUDA = @FECHA_ULT_LIB_DEUDA,
        DNI_DESDE_CUIT = @DNI_DESDE_CUIT
    WHERE CUIL = @CUIL;
END;

/*
EXEC [dbo].[AntoUpdate_Proveedores]
    @RAZON_SOCIAL = 'Empresa Actualizada',
    @CUIL = '20327462561',
    @PROVINCIA = 'Catamarca',
    @LOCALIDAD = 'Mar del Plata',
    @CALLE = 'Calle Actualizada',
    @CALLE_NRO = '123',
    @DPTO = 'B',
    @PISO = '1',
    @EMAIL = 'empresa.actualizada@ejemplo.com',
    @CONDICION_CTA = 'Activa',
    @CONDICION_EN_AFIP = 'Inscripto',
    @CONDICION_DGR = 'Con Deuda',
    @CONDICION_GCIA = 'Irregular',
    @CONDICION_EMPLEADOR = 'Contribuyente',
    @FORMA_JURIDICA = 'Sociedad de Responsabilidad Limitada',
    @FECHA_ULT_LIB_DEUDA = '2024-12-01',
    @DNI_DESDE_CUIT = null;

	*/