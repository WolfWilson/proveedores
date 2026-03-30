USE [Gestion]
GO
/****** Object:  StoredProcedure [dbo].[AntoInsert_Proveedores_By_CUIL]    Script Date: 30/03/2026 10:49:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[AntoInsert_Proveedores_By_CUIL]
    @RAZON_SOCIAL      VARCHAR(200),
    @CUIL              CHAR(11),
    @PROVINCIA         VARCHAR(50),
    @LOCALIDAD         VARCHAR(50),
    @CALLE             VARCHAR(50),
    @CALLE_NRO         CHAR(6),
    @DPTO              VARCHAR(50),
    @PISO              VARCHAR(50),
    @EMAIL             VARCHAR(50),
    @CONDICION_CTA     VARCHAR(30),
    @CONDICION_EN_AFIP VARCHAR(30),
    @CONDICION_DGR     VARCHAR(30),
    @CONDICION_GCIA    VARCHAR(30),
    @CONDICION_EMPLEADOR VARCHAR(30),
    @FORMA_JURIDICA    VARCHAR(80),
    @FECHA_ULT_LIB_DEUDA DATETIME,
    @DNI_DESDE_CUIT    INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Verificar si el CUIL ya existe en la tabla
    IF EXISTS (SELECT 1 FROM PROVEEDORES WHERE CUIL = @CUIL)
    BEGIN
        PRINT 'El CUIL ya existe en la tabla. Inserción cancelada.';
        RETURN;
    END

    -- Insertar los datos en la tabla PROVEEDORES
    INSERT INTO PROVEEDORES (
        RAZON_SOCIAL,
        CUIL,
        PROVINCIA,
        LOCALIDAD,
        CALLE,
        CALLE_NRO,
        DPTO,
        PISO,
        EMAIL,
        CONDICION_CTA,
        CONDICION_EN_AFIP,
        CONDICION_DGR,
        CONDICION_GCIA,
        CONDICION_EMPLEADOR,
        FORMA_JURIDICA,
        FECHA_ULT_LIB_DEUDA,
        DNI_DESDE_CUIT
    )
    VALUES (
        @RAZON_SOCIAL,
        @CUIL,
        @PROVINCIA,
        @LOCALIDAD,
        @CALLE,
        @CALLE_NRO,
        @DPTO,
        @PISO,
        @EMAIL,
        @CONDICION_CTA,
        @CONDICION_EN_AFIP,
        @CONDICION_DGR,
        @CONDICION_GCIA,
        @CONDICION_EMPLEADOR,
        @FORMA_JURIDICA,
        @FECHA_ULT_LIB_DEUDA,
        @DNI_DESDE_CUIT
    );

    PRINT 'Registro insertado exitosamente.';
END
