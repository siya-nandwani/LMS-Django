from django.db import models


class ProductCategory(models.Model):
    categoryid = models.IntegerField(
        db_column='CategoryID',
        primary_key=True
    )

    categoryname = models.CharField(
        db_column='CategoryName',
        max_length=100,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'PRODUCT_CATEGORY'

    def __str__(self):
        return str(self.categoryname or f"Category {self.categoryid}")

class Product(models.Model):
    productid = models.IntegerField(
        db_column='ProductID',
        primary_key=True
    )

    productname = models.CharField(
        db_column='ProductName',
        max_length=200,
        blank=True,
        null=True
    )

    categoryid = models.ForeignKey(
        ProductCategory,
        models.DO_NOTHING,
        db_column='CategoryID'
    )

    is_active = models.SmallIntegerField(
        db_column='Is_Active',
        default=True,
        blank=True,
        null=True
    )

    added_by = models.CharField(
        db_column='Added_By',
        max_length=255,
        blank=True,
        null=True
    )

    added_dts = models.TimeField(
        db_column='Added_Dts',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'PRODUCT'

    def __str__(self):
        return str(self.productname or f"Product {self.productid}")


class Region(models.Model):
    regionid = models.IntegerField(
        db_column='RegionID',
        primary_key=True
    )

    regionname = models.CharField(
        db_column='RegionName',
        max_length=100,
        blank=True,
        null=True
    )

    added_by = models.CharField(
        db_column='Added_By',
        max_length=255,
        blank=True,
        null=True
    )

    added_dts = models.TimeField(
        db_column='Added_Dts',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'REGION'

    def __str__(self):
        return str(self.regionname or f"Region {self.regionid}")


class Lead(models.Model):
    leadid = models.IntegerField(db_column='LeadID', primary_key=True)

    personname = models.CharField(
        db_column='PersonName',
        max_length=100,
        blank=True,
        null=True
    )

    gender = models.CharField(
        db_column='Gender',
        max_length=20,
        blank=True,
        null=True
    )

    companyname = models.CharField(
        db_column='CompanyName',
        max_length=200,
        blank=True,
        null=True
    )

    contactno = models.CharField(
        db_column='ContactNo',
        max_length=20,
        blank=True,
        null=True
    )

    email = models.CharField(
        db_column='Email',
        max_length=100,
        blank=True,
        null=True
    )

    city = models.CharField(
        db_column='City',
        max_length=100,
        blank=True,
        null=True
    )

    state = models.CharField(
        db_column='State',
        max_length=100,
        blank=True,
        null=True
    )

    territoryid = models.ForeignKey(
        'Territory',
        models.DO_NOTHING,
        db_column='TerritoryID'
    )

    regionid = models.ForeignKey(
        'Region',
        models.DO_NOTHING,
        db_column='RegionID'
    )

    productid = models.ForeignKey(
        'Product',
        models.DO_NOTHING,
        db_column='ProductID'
    )

    statusid = models.ForeignKey(
        'LeadStatus',
        models.DO_NOTHING,
        db_column='StatusID'
    )

    leadsourceid = models.ForeignKey(
        'LeadSource',
        models.DO_NOTHING,
        db_column='LeadSourceID'
    )

    businessneed = models.CharField(
        db_column='BusinessNeed',
        max_length=500,
        blank=True,
        null=True
    )

    lead_gen_date = models.DateField(
        db_column='Lead_Gen_Date',
        blank=True,
        null=True
    )

    added_by = models.CharField(
        db_column='Added_By',
        max_length=255,
        blank=True,
        null=True
    )

    added_dts = models.TimeField(
        db_column='Added_Dts',
        blank=True,
        null=True
    )

    executiveid = models.IntegerField(
        db_column='ExecutiveID',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'LEAD'

class Territory(models.Model):
    territoryid = models.IntegerField(
        db_column='TerritoryID',
        primary_key=True
    )

    territoryname = models.CharField(
        db_column='TerritoryName',
        max_length=150,
        blank=True,
        null=True
    )

    regionid = models.IntegerField(
        db_column='RegionID',
        blank=True,
        null=True
    )

    added_by = models.CharField(
        db_column='Added_By',
        max_length=255,
        blank=True,
        null=True
    )

    added_dts = models.TimeField(
        db_column='Added_Dts',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'TERRITORY'

    def __str__(self):
        return str(self.territoryname or f"Territory {self.territoryid}")
    
class LeadStatus(models.Model):
    statusid = models.IntegerField(
        db_column='StatusID',
        primary_key=True
    )

    statusname = models.CharField(
        db_column='StatusName',
        max_length=100,
        blank=True,
        null=True
    )

    added_by = models.CharField(
        db_column='Added_By',
        max_length=255,
        blank=True,
        null=True
    )

    added_dts = models.TimeField(
        db_column='Added_Dts',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'LEAD_STATUS'

    def __str__(self):
        return str(self.statusname or f"Status {self.statusid}")
    
class LeadSource(models.Model):
    leadsourceid = models.IntegerField(
        db_column='LeadSourceID',
        primary_key=True
    )

    leadsourcename = models.CharField(
        db_column='LeadSourceName',
        max_length=100,
        blank=True,
        null=True
    )

    added_by = models.CharField(
        db_column='Added_By',
        max_length=255,
        blank=True,
        null=True
    )

    added_dts = models.TimeField(
        db_column='Added_Dts',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'LEAD_SOURCE'

    def __str__(self):
        return str(self.leadsourcename or f"LeadSource {self.leadsourceid}")