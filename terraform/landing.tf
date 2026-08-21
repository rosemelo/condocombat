data "netlify_site" "landing" {
  site_id = var.netlify_site_id
}

resource "netlify_environment_variable" "landing_public_url" {
  site_id = data.netlify_site.landing.id
  key     = "PUBLIC_APP_URL"
  values = [
    {
      value   = render_web_service.frontend.url
      context = "all"
    }
  ]
}

resource "terraform_data" "landing_deploy" {
  triggers_replace = [
    data.netlify_site.landing.id,
    render_web_service.frontend.url
  ]

  provisioner "local-exec" {
    command = "npx netlify-cli deploy --dir=${path.module}/../landing/dist --prod --auth=${var.netlify_api_token} --site=${data.netlify_site.landing.id}"
  }

  depends_on = [
    netlify_environment_variable.landing_public_url
  ]
}