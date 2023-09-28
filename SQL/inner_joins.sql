Select Licence_Details.*,
 Licence_type_master.name as LicenseType,
 operatormaster.*,
 geographicregionmaster.Name as Region,
 operator_user.*licence_details From Licence_Details
    Inner Join Licence_type_master ON Licence_Details.fk_licence_type = Licence_type_master.id
    Inner Join operatormaster on Licence_Details.fk_operator_master = operatormaster.id
    Inner Join operator_user on operator_user.fk_operator_master = operatormaster.id
    Inner Join geographicregionmaster on Licence_Details.fk_geographic_Region = geographicregionmaster.id
    Inner Join license_status_master on Licence_Details.fk_license_status = license_status_master.id