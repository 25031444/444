   from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
   from flask_login import login_required
   from app import db
   from app.models.business import ServiceType, Service
   from app.forms.business import ServiceTypeForm

   bp = Blueprint('business', __name__)

   # 服务类型管理
   @bp.route('/service_types')
   @login_required
   def service_types():
       """服务类型管理"""
       service_types = ServiceType.query.all()
       return render_template('business/service_types.html', service_types=service_types)

   @bp.route('/add_service_type', methods=['GET', 'POST'])
   @login_required
   def add_service_type():
       """添加服务类型"""
       form = ServiceTypeForm()
       if form.validate_on_submit():
           service_type = ServiceType(
               name=form.name.data,
               description=form.description.data,
               is_active=form.is_active.data
           )
           db.session.add(service_type)
           db.session.commit()
           flash('服务类型添加成功')
           return redirect(url_for('business.service_types'))
       return render_template('business/service_type_form.html', form=form, title='添加服务类型')

   @bp.route('/edit_service_type/<int:type_id>', methods=['GET', 'POST'])
   @login_required
   def edit_service_type(type_id):
       """编辑服务类型"""
       service_type = ServiceType.query.get_or_404(type_id)
       form = ServiceTypeForm(obj=service_type)
       if form.validate_on_submit():
           form.populate_obj(service_type)
           db.session.commit()
           flash('服务类型更新成功')
           return redirect(url_for('business.service_types'))
       return render_template('business/service_type_form.html', form=form, title='编辑服务类型')

   @bp.route('/delete_service_type', methods=['POST'])
   @login_required
   def delete_service_type():
       """删除服务类型"""
       type_id = request.form.get('id')
       service_type = ServiceType.query.get_or_404(type_id)
       
       # 检查是否有服务使用此类型
       services = Service.query.filter_by(type_id=type_id).first()
       if services:
           return jsonify({"code": 1, "msg": "该类型下有服务项目，无法删除"})
       
       db.session.delete(service_type)
       db.session.commit()
       return jsonify({"code": 0, "msg": "删除成功"})

   # 服务管理
   @bp.route('/services')
   @login_required
   def services():
       """服务管理"""
       services = Service.query.all()
       return render_template('business/services.html', services=services)